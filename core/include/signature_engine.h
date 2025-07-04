#ifndef CANINANA_CORE_INCLUDE_SIGNATURE_ENGINE_H_
#define CANINANA_CORE_INCLUDE_SIGNATURE_ENGINE_H_

#include <cstdint>
#include <istream>
#include <string>
#include <unordered_map>
#include <vector>

#include "file_analyzer.h"

namespace caninana {
namespace core {

class SignatureEngine {
 public:
  struct Signature {
    std::string name;
    std::string pattern;
    FileType target_type;
    uint8_t severity;
  };

  struct ScanResult {
    enum class ScanStatus {
      COMPLETE,
      TIMEOUT_ERROR,
    };

    ScanStatus status{ScanStatus::COMPLETE};
    bool threat_detected{false};
    std::vector<std::string> detected_signatures;
    uint8_t max_severity{0};
  };

  /**
   * @brief Loads and parses a signature database from a JSON file.
   *
   * @param signature_db_path The path to the JSON signature database file.
   * @throws FileAccessError if the database file cannot be opened.
   * @throws DatabaseParseError if the JSON is malformed.
   */
  void LoadSignatures(const std::string& signature_db_path);

  ScanResult Scan(std::istream& file_stream, const FileInfo& file_info);

 private:
  FileType FileTypeFromString(const std::string& type_str) const;

  std::vector<Signature> signatures_;
  std::unordered_map<FileType, std::vector<size_t>> type_index_;
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_SIGNATURE_ENGINE_H_