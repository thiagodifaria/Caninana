#include "quarantine_manager.h"

#include <nlohmann/json.hpp>

#include <chrono>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <random>
#include <sstream>

#include "file_exception.h"
#include "security_logger.h"

namespace caninana {
namespace core {

void to_json(nlohmann::json& j, const QuarantineEntry& e) {
  j = nlohmann::json{{"quarantine_id", e.quarantine_id},
                     {"original_path", e.original_path},
                     {"quarantine_date", e.quarantine_date},
                     {"threat_name", e.threat_name}};
}

void from_json(const nlohmann::json& j, QuarantineEntry& e) {
  j.at("quarantine_id").get_to(e.quarantine_id);
  j.at("original_path").get_to(e.original_path);
  j.at("quarantine_date").get_to(e.quarantine_date);
  j.at("threat_name").get_to(e.threat_name);
}

namespace {
const std::vector<char> kXorKey = {'C', 'A', 'N', 'I', 'N', 'A', 'N', 'A'};
const std::string kMetadataFileName = "ledger.json";
std::string GenerateUUID() {
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<> dis(0, 255);
  std::stringstream ss;
  ss << std::hex << std::setw(2) << std::setfill('0');
  for (int i = 0; i < 16; ++i) {
    if (i == 4 || i == 6 || i == 8 || i == 10) ss << "-";
    ss << dis(gen);
  }
  return ss.str();
}
std::string GetCurrentTimestamp() {
  const auto now = std::chrono::system_clock::now();
  const auto in_time_t = std::chrono::system_clock::to_time_t(now);
  std::stringstream ss;
  ss << std::put_time(std::gmtime(&in_time_t), "%Y-%m-%dT%H:%M:%SZ");
  return ss.str();
}
}  // namespace

QuarantineManager::QuarantineManager(const std::string& root_path) {
  if (!root_path.empty()) {
    quarantine_path_ =
        (std::filesystem::path(root_path) / "quarantine").string();
  } else {
    const char* home_dir = getenv("HOME");
    if (!home_dir) home_dir = getenv("USERPROFILE");
    if (home_dir) {
      quarantine_path_ =
          (std::filesystem::path(home_dir) / ".caninana" / "quarantine")
              .string();
    } else {
      quarantine_path_ = "caninana_quarantine";
    }
  }
  metadata_path_ =
      (std::filesystem::path(quarantine_path_) / kMetadataFileName).string();
  InitializeQuarantineDirectory();
}

void QuarantineManager::InitializeQuarantineDirectory() {
  try {
    std::filesystem::create_directories(quarantine_path_);
    if (!std::filesystem::exists(metadata_path_)) {
      std::ofstream ledger_file(metadata_path_);
      if (ledger_file.is_open()) {
        ledger_file << nlohmann::json::array() << std::endl;
      } else {
        throw InitializationError(
            "Failed to create empty metadata ledger at: " + metadata_path_);
      }
    }
  } catch (const std::filesystem::filesystem_error& e) {
    throw InitializationError("Failed to create quarantine directory '" +
                              quarantine_path_ + "'. Error: " + e.what());
  }
}

void QuarantineManager::QuarantineFile(
    const std::string& filepath, const SignatureEngine::ScanResult& threat) {
  if (!std::filesystem::exists(filepath)) {
    throw FileAccessError("Quarantine failed. File does not exist: " +
                          filepath);
  }

  QuarantineEntry new_entry;
  new_entry.quarantine_id = GenerateUUID();
  new_entry.original_path = std::filesystem::absolute(filepath).string();
  new_entry.quarantine_date = GetCurrentTimestamp();
  new_entry.threat_name = threat.detected_signatures.empty()
                              ? "UnknownThreat"
                              : threat.detected_signatures.front();

  const std::string quarantined_filepath =
      (std::filesystem::path(quarantine_path_) / new_entry.quarantine_id)
          .string();

  try {
    std::filesystem::rename(filepath, quarantined_filepath);
  } catch (const std::filesystem::filesystem_error& e) {
    throw QuarantineError("Quarantine failed. Could not move file '" +
                          filepath + "' to '" + quarantined_filepath +
                          "'. Error: " + e.what());
  }

  if (!ProcessFileXOR(quarantined_filepath)) {
    // Attempt to move the file back as a recovery measure.
    try {
      std::filesystem::rename(quarantined_filepath, filepath);
    } catch (...) {
    }
    throw QuarantineError(
        "Quarantine failed. Could not neutralize file content for ID: " +
        new_entry.quarantine_id);
  }

  auto entries = ListQuarantinedFiles();
  entries.push_back(new_entry);
  std::ofstream ledger_file(metadata_path_);
  if (!ledger_file.is_open()) {
    // Critical failure: file is quarantined but not tracked. Attempt recovery.
    try {
      ProcessFileXOR(quarantined_filepath);  // De-neutralize
      std::filesystem::rename(quarantined_filepath, filepath);
    } catch (...) {
    }
    throw QuarantineError(
        "Quarantine failed. Could not open metadata ledger to record entry for ID: " +
        new_entry.quarantine_id);
  }

  ledger_file << nlohmann::json(entries).dump(2);
  SecurityLogger::GetInstance().Log(
      SecurityLogger::LogLevel::WARNING, "QuarantineManager",
      "File quarantined. Original path: " + new_entry.original_path +
          ", ID: " + new_entry.quarantine_id);
}

void QuarantineManager::RestoreFile(const std::string& quarantine_id) {
  auto entries = ListQuarantinedFiles();
  auto it = std::find_if(
      entries.begin(), entries.end(),
      [&](const QuarantineEntry& e) { return e.quarantine_id == quarantine_id; });

  if (it == entries.end()) {
    throw QuarantineError("Restore failed. ID not found in ledger: " +
                          quarantine_id);
  }

  const QuarantineEntry entry_to_restore = *it;
  const std::string quarantined_filepath =
      (std::filesystem::path(quarantine_path_) / entry_to_restore.quarantine_id)
          .string();

  if (!std::filesystem::exists(quarantined_filepath)) {
    throw QuarantineError(
        "Restore failed. File missing from storage. ID: " + quarantine_id);
  }

  if (!ProcessFileXOR(quarantined_filepath)) {
    throw QuarantineError("Restore failed. Could not de-neutralize file. ID: " +
                          quarantine_id);
  }

  try {
    std::filesystem::path original_parent_path =
        std::filesystem::path(entry_to_restore.original_path).parent_path();
    if (!original_parent_path.empty()) {
      std::filesystem::create_directories(original_parent_path);
    }
    std::filesystem::rename(quarantined_filepath,
                            entry_to_restore.original_path);
  } catch (const std::filesystem::filesystem_error& e) {
    ProcessFileXOR(quarantined_filepath);  // Re-neutralize on failure.
    throw QuarantineError("Restore failed. Could not move file to original location '" +
                          entry_to_restore.original_path +
                          "'. Error: " + e.what());
  }

  entries.erase(it);
  std::ofstream ledger_file(metadata_path_);
  if (ledger_file.is_open()) {
    ledger_file << nlohmann::json(entries).dump(2);
  } else {
    SecurityLogger::GetInstance().Log(
        SecurityLogger::LogLevel::CRITICAL, "QuarantineManager",
        "Restore succeeded, but failed to update metadata ledger for ID: " +
            quarantine_id);
  }

  SecurityLogger::GetInstance().Log(
      SecurityLogger::LogLevel::INFO, "QuarantineManager",
      "File restored. ID: " + quarantine_id +
          ", Path: " + entry_to_restore.original_path);
}

std::vector<QuarantineEntry> QuarantineManager::ListQuarantinedFiles() const {
  std::vector<QuarantineEntry> entries;
  std::ifstream ledger_file(metadata_path_);
  if (!ledger_file.is_open()) return entries;
  try {
    nlohmann::json j;
    ledger_file >> j;
    if (j.is_array()) entries = j.get<std::vector<QuarantineEntry>>();
  } catch (const nlohmann::json::exception&) {
    return {};
  }
  return entries;
}

bool QuarantineManager::ProcessFileXOR(const std::string& filepath) const {
  if (kXorKey.empty()) return false;
  std::fstream file(filepath, std::ios::in | std::ios::out | std::ios::binary);
  if (!file.is_open()) return false;
  char buffer[4096];
  size_t key_index = 0;
  while (file.read(buffer, sizeof(buffer)) || file.gcount() > 0) {
    std::streamsize bytes_read = file.gcount();
    for (std::streamsize i = 0; i < bytes_read; ++i) {
      buffer[i] ^= kXorKey[key_index];
      key_index = (key_index + 1) % kXorKey.size();
    }
    file.seekp(static_cast<std::streamoff>(file.tellg()) - bytes_read);
    file.write(buffer, bytes_read);
    file.flush();
  }
  return true;
}

}  // namespace core
}  // namespace caninana