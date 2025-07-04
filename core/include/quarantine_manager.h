#ifndef CANINANA_CORE_INCLUDE_QUARANTINE_MANAGER_H_
#define CANINANA_CORE_INCLUDE_QUARANTINE_MANAGER_H_

#include <string>
#include <vector>

#include "signature_engine.h"

namespace caninana {
namespace core {

struct QuarantineEntry {
  std::string quarantine_id;
  std::string original_path;
  std::string quarantine_date;
  std::string threat_name;
};

class QuarantineManager {
 public:
  /**
   * @brief Constructs the QuarantineManager.
   * @param root_path The root directory for application data.
   * @throws InitializationError if the quarantine directory cannot be created.
   */
  explicit QuarantineManager(const std::string& root_path = "");

  /**
   * @brief Moves a file to quarantine.
   * @param filepath Path to the malicious file.
   * @param threat The scan result that triggered the action.
   * @throws FileAccessError if the source file doesn't exist.
   * @throws QuarantineError on failure to move, neutralize, or log metadata.
   */
  void QuarantineFile(const std::string& filepath,
                      const SignatureEngine::ScanResult& threat);

  /**
   * @brief Restores a file from quarantine.
   * @param quarantine_id The unique ID of the file to restore.
   * @throws QuarantineError if the ID is not found, the file is missing, or
   * the restore operation fails.
   */
  void RestoreFile(const std::string& quarantine_id);

  std::vector<QuarantineEntry> ListQuarantinedFiles() const;

 private:
  std::string quarantine_path_;
  std::string metadata_path_;

  void InitializeQuarantineDirectory();
  bool ProcessFileXOR(const std::string& filepath) const;
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_QUARANTINE_MANAGER_H_