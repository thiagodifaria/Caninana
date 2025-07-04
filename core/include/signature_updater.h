#ifndef CANINANA_CORE_INCLUDE_SIGNATURE_UPDATER_H_
#define CANINANA_CORE_INCLUDE_SIGNATURE_UPDATER_H_

#include <string>

namespace caninana {
namespace core {

/**
 * @class SignatureUpdater
 * @brief Manages the process of updating the signature database from a remote
 * source.
 */
class SignatureUpdater {
 public:
  /**
   * @brief Constructs the updater with a base URL for update files.
   * @param base_url The URL prefix where 'latest_version.txt' and
   * 'signatures.json' are hosted.
   */
  explicit SignatureUpdater(const std::string& base_url);

  /**
   * @brief Checks for a new signature database, downloads, validates, and
   * applies it.
   *
   * @param current_db_path The path to the current signature database file
   * (e.g., 'default.json').
   * @return True if a new version was successfully applied, false otherwise.
   * @throws FileAccessError on local file issues.
   * @throws std::runtime_error on network errors or validation failures.
   */
  bool CheckForUpdates(const std::string& current_db_path);

 private:
  /**
   * @brief Reads the 'version' field from a local JSON database file.
   * @param db_path Path to the local database.
   * @return The version string, or "0" if not found or invalid.
   */
  std::string GetLocalVersion(const std::string& db_path);

  std::string base_url_;
  std::string version_url_;
  std::string database_url_;
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_SIGNATURE_UPDATER_H_