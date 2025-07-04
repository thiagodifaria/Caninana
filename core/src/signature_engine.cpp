#include "signature_engine.h"

#include <nlohmann/json.hpp>

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iterator>
#include <map>
#include <queue>
#include <set>
#include <sstream>

#include "file_exception.h"
#include "performance_monitor.h"
#include "security_logger.h"

namespace caninana {
namespace core {

// AhoCorasickMatcher implementation is unchanged and omitted for brevity.
namespace {
class AhoCorasickMatcher {
 public:
  void Build(
      const std::vector<const SignatureEngine::Signature*>& signatures) {
    nodes_.clear();
    nodes_.emplace_back();
    pattern_map_.clear();
    for (const auto* sig : signatures) {
      if (!sig->pattern.empty()) {
        AddPattern(sig);
        pattern_map_[sig->pattern] = sig;
      }
    }
    ComputeFailureLinks();
  }
  bool ScanStream(
      std::istream& stream, const PerformanceMonitor& monitor,
      std::chrono::seconds timeout,
      std::vector<const SignatureEngine::Signature*>& out_matches) const {
    std::set<std::string> detected_patterns;
    size_t current_node_idx = 0;
    std::vector<char> buffer(8192);
    int iteration_count = 0;
    while (stream) {
      if (++iteration_count % 16 == 0 && monitor.HasTimedOut(timeout)) {
        return true;
      }
      stream.read(buffer.data(), buffer.size());
      std::streamsize bytes_read = stream.gcount();
      if (bytes_read == 0) break;
      for (std::streamsize i = 0; i < bytes_read; ++i) {
        char c = buffer[i];
        current_node_idx = FindNextNode(current_node_idx, c);
        size_t temp_node_idx = current_node_idx;
        while (temp_node_idx != 0) {
          if (!nodes_[temp_node_idx].output_patterns.empty()) {
            detected_patterns.insert(
                nodes_[temp_node_idx].output_patterns.begin(),
                nodes_[temp_node_idx].output_patterns.end());
          }
          temp_node_idx = nodes_[temp_node_idx].failure_link;
        }
      }
    }
    for (const auto& pattern : detected_patterns) {
      auto it = pattern_map_.find(pattern);
      if (it != pattern_map_.end()) {
        out_matches.push_back(it->second);
      }
    }
    return false;
  }

 private:
  struct Node {
    std::map<char, size_t> transitions;
    size_t failure_link{0};
    std::vector<std::string> output_patterns;
  };
  std::vector<Node> nodes_;
  std::unordered_map<std::string, const SignatureEngine::Signature*>
      pattern_map_;
  void AddPattern(const SignatureEngine::Signature* sig) {
    size_t current_node_idx = 0;
    for (char c : sig->pattern) {
      auto it = nodes_[current_node_idx].transitions.find(c);
      if (it == nodes_[current_node_idx].transitions.end()) {
        size_t new_node_idx = nodes_.size();
        nodes_[current_node_idx].transitions[c] = new_node_idx;
        nodes_.emplace_back();
        current_node_idx = new_node_idx;
      } else {
        current_node_idx = it->second;
      }
    }
    nodes_[current_node_idx].output_patterns.push_back(sig->pattern);
  }
  void ComputeFailureLinks() {
    std::queue<size_t> q;
    for (auto const& [key, val] : nodes_[0].transitions) {
      q.push(val);
    }
    while (!q.empty()) {
      size_t current_node_idx = q.front();
      q.pop();
      for (auto const& [character, next_node_idx] :
           nodes_[current_node_idx].transitions) {
        q.push(next_node_idx);
        size_t failure_node_idx = nodes_[current_node_idx].failure_link;
        while (failure_node_idx != 0 &&
               nodes_[failure_node_idx].transitions.find(character) ==
                   nodes_[failure_node_idx].transitions.end()) {
          failure_node_idx = nodes_[failure_node_idx].failure_link;
        }
        auto it = nodes_[failure_node_idx].transitions.find(character);
        if (it != nodes_[failure_node_idx].transitions.end()) {
          nodes_[next_node_idx].failure_link = it->second;
        } else {
          nodes_[next_node_idx].failure_link = 0;
        }
        size_t inherited_output_node = nodes_[next_node_idx].failure_link;
        if (!nodes_[inherited_output_node].output_patterns.empty()) {
          nodes_[next_node_idx].output_patterns.insert(
              nodes_[next_node_idx].output_patterns.end(),
              nodes_[inherited_output_node].output_patterns.begin(),
              nodes_[inherited_output_node].output_patterns.end());
        }
      }
    }
  }
  size_t FindNextNode(size_t current_node_idx, char character) const {
    while (current_node_idx != 0 &&
           nodes_[current_node_idx].transitions.find(character) ==
               nodes_[current_node_idx].transitions.end()) {
      current_node_idx = nodes_[current_node_idx].failure_link;
    }
    auto it = nodes_[current_node_idx].transitions.find(character);
    if (it != nodes_[current_node_idx].transitions.end()) {
      return it->second;
    }
    return 0;
  }
};
}  // namespace

void SignatureEngine::LoadSignatures(const std::string& signature_db_path) {
  signatures_.clear();
  type_index_.clear();

  std::ifstream db_file(signature_db_path);
  if (!db_file.is_open()) {
    throw FileAccessError("Failed to open signature database: " +
                          signature_db_path);
  }

  nlohmann::json db_json;
  try {
    db_file >> db_json;
  } catch (const nlohmann::json::parse_error& e) {
    throw DatabaseParseError(
        "Failed to parse signature database. Invalid JSON: " +
        std::string(e.what()));
  }

  if (!db_json.contains("signatures") || !db_json["signatures"].is_array()) {
    throw DatabaseParseError(
        "Signature database is malformed: missing 'signatures' array.");
  }

  for (const auto& sig_json : db_json["signatures"]) {
    if (!sig_json.is_object()) continue;
    Signature new_signature;
    new_signature.name = sig_json.value("name", "Unnamed Signature");
    new_signature.pattern = sig_json.value("pattern", "");
    new_signature.target_type =
        FileTypeFromString(sig_json.value("file_type", "any"));
    new_signature.severity = sig_json.value("severity", 0);

    if (new_signature.pattern.empty()) {
      continue;
    }
    signatures_.push_back(new_signature);
    const size_t new_index = signatures_.size() - 1;
    type_index_[new_signature.target_type].push_back(new_index);
  }
}

SignatureEngine::ScanResult SignatureEngine::Scan(std::istream& file_stream,
                                                  const FileInfo& file_info) {
  ScanResult result;
  const auto kScanTimeout = std::chrono::seconds(30);
  std::vector<const Signature*> signatures_to_check;
  std::set<size_t> added_indices;

  auto it = type_index_.find(file_info.type);
  if (it != type_index_.end()) {
    for (size_t index : it->second) {
      if (added_indices.find(index) == added_indices.end()) {
        signatures_to_check.push_back(&signatures_[index]);
        added_indices.insert(index);
      }
    }
  }
  it = type_index_.find(FileType::UNKNOWN);
  if (it != type_index_.end()) {
    for (size_t index : it->second) {
      if (added_indices.find(index) == added_indices.end()) {
        signatures_to_check.push_back(&signatures_[index]);
        added_indices.insert(index);
      }
    }
  }

  if (signatures_to_check.empty()) {
    SecurityLogger::GetInstance().Log(SecurityLogger::LogLevel::INFO,
                                      "SignatureEngine",
                                      "Scan completed (no relevant signatures).");
    return result;
  }

  AhoCorasickMatcher matcher;
  matcher.Build(signatures_to_check);
  PerformanceMonitor monitor;
  monitor.Start();
  std::vector<const Signature*> matched_signatures;
  bool timed_out = matcher.ScanStream(file_stream, monitor, kScanTimeout,
                                      matched_signatures);

  if (timed_out) {
    result.status = ScanResult::ScanStatus::TIMEOUT_ERROR;
    result.threat_detected = true;
    result.max_severity = 8;
    result.detected_signatures.push_back("Error.ScanTimeoutExceeded");
    SecurityLogger::GetInstance().Log(SecurityLogger::LogLevel::LOG_ERROR,
                                      "SignatureEngine", "Scan timed out.");
  } else if (!matched_signatures.empty()) {
    result.status = ScanResult::ScanStatus::COMPLETE;
    result.threat_detected = true;
    std::stringstream sig_names;
    for (const Signature* sig : matched_signatures) {
      result.detected_signatures.push_back(sig->name);
      result.max_severity = std::max(result.max_severity, sig->severity);
      sig_names << sig->name << ", ";
    }
    std::string sig_list = sig_names.str();
    if (sig_list.length() > 2) {
      sig_list.resize(sig_list.length() - 2);
    }
    SecurityLogger::GetInstance().Log(
        SecurityLogger::LogLevel::CRITICAL, "SignatureEngine",
        "Threat detected. Signatures: [" + sig_list + "]");
  } else {
    SecurityLogger::GetInstance().Log(SecurityLogger::LogLevel::INFO,
                                      "SignatureEngine",
                                      "Scan completed (clean).");
  }

  return result;
}

FileType SignatureEngine::FileTypeFromString(
    const std::string& type_str) const {
  if (type_str == "executable") return FileType::EXECUTABLE;
  if (type_str == "archive") return FileType::ARCHIVE;
  if (type_str == "document") return FileType::DOCUMENT;
  if (type_str == "image") return FileType::IMAGE;
  if (type_str == "script") return FileType::SCRIPT;
  return FileType::UNKNOWN;
}

}  // namespace core
}  // namespace caninana