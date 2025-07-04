#include "signature_updater.h"

#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

#include <filesystem>
#include <fstream>

#include "file_exception.h"
#include "security_logger.h"
#include "signature_engine.h"

namespace caninana {
namespace core {

SignatureUpdater::SignatureUpdater(const std::string& base_url)
    : base_url_(base_url) {
  if (base_url_.back() != '/') {
    base_url_ += '/';
  }
  version_url_ = base_url_ + "latest_version.txt";
  database_url_ = base_url_ + "signatures.json";
}

std::string SignatureUpdater::GetLocalVersion(const std::string& db_path) {
  try {
    std::ifstream db_file(db_path);
    if (!db_file.is_open()) {
      return "0";  // If file doesn't exist, version is effectively 0.
    }
    nlohmann::json db_json;
    db_file >> db_json;
    return db_json.value("version", "0");
  } catch (const std::exception&) {
    return "0";  // If parsing fails, treat version as 0.
  }
}

bool SignatureUpdater::CheckForUpdates(const std::string& current_db_path) {
  auto& logger = SecurityLogger::GetInstance();
  logger.Log(SecurityLogger::LogLevel::INFO, "SignatureUpdater",
             "Checking for updates...");

  const std::string local_version = GetLocalVersion(current_db_path);
  logger.Log(SecurityLogger::LogLevel::INFO, "SignatureUpdater",
             "Local database version: " + local_version);

  cpr::Response r = cpr::Get(cpr::Url{version_url_});
  if (r.status_code != 200) {
    throw std::runtime_error("Failed to download version file from " +
                             version_url_ + ". Status code: " +
                             std::to_string(r.status_code));
  }
  std::string remote_version = r.text;
  // Trim whitespace/newlines from remote version
  remote_version.erase(
      remote_version.find_last_not_of(" \n\r\t") + 1);

  logger.Log(SecurityLogger::LogLevel::INFO, "SignatureUpdater",
             "Remote database version: " + remote_version);

  if (remote_version <= local_version) {
    logger.Log(SecurityLogger::LogLevel::INFO, "SignatureUpdater",
               "Signature database is already up to date.");
    return false;
  }

  logger.Log(SecurityLogger::LogLevel::WARNING, "SignatureUpdater",
             "New version available. Downloading from " + database_url_);

  const std::string tmp_db_path = current_db_path + ".tmp";
  std::ofstream tmp_file(tmp_db_path, std::ios::binary);
  if (!tmp_file) {
      throw FileAccessError("Failed to open temporary file for writing: " + tmp_db_path);
  }
  cpr::Response db_response = cpr::Download(tmp_file, cpr::Url{database_url_});
  tmp_file.close();

  if (db_response.status_code != 200) {
    std::filesystem::remove(tmp_db_path);
    throw std::runtime_error("Failed to download database file. Status code: " +
                             std::to_string(db_response.status_code));
  }

  logger.Log(SecurityLogger::LogLevel::INFO, "SignatureUpdater",
             "Download complete. Validating new database...");

  try {
    SignatureEngine validator;
    validator.LoadSignatures(tmp_db_path);
    logger.Log(SecurityLogger::LogLevel::INFO, "SignatureUpdater",
               "New database is valid.");
  } catch (const std::exception& e) {
    std::filesystem::remove(tmp_db_path);
    logger.Log(SecurityLogger::LogLevel::LOG_ERROR, "SignatureUpdater",
               "Downloaded database failed validation: " + std::string(e.what()));
    throw std::runtime_error("Downloaded database is corrupt or invalid.");
  }

  try {
    std::filesystem::rename(tmp_db_path, current_db_path);
    logger.Log(SecurityLogger::LogLevel::WARNING, "SignatureUpdater",
               "Successfully updated signature database to version " +
                   remote_version);
  } catch (const std::filesystem::filesystem_error& e) {
    std::filesystem::remove(tmp_db_path);
    throw FileAccessError("Failed to apply update: " + std::string(e.what()));
  }

  return true;
}

}  // namespace core
}  // namespace caninana