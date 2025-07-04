#include "security_logger.h"

#include <chrono>
#include <filesystem>
#include <iomanip>
#include <iostream>
#include <sstream>  // FIX: Missing header for std::stringstream

namespace caninana {
namespace core {

SecurityLogger& SecurityLogger::GetInstance() {
  // This is thread-safe in C++11 and later.
  static SecurityLogger instance;
  return instance;
}

SecurityLogger::SecurityLogger() {
  // Determine the application data directory, co-locating with other data like
  // the quarantine.
  std::string app_data_path;
  const char* home_dir = getenv("HOME");  // POSIX
  if (!home_dir) {
    home_dir = getenv("USERPROFILE");  // Windows
  }
  if (home_dir) {
    app_data_path = (std::filesystem::path(home_dir) / ".caninana").string();
  } else {
    app_data_path = ".";  // Fallback to current directory.
  }

  try {
    std::filesystem::create_directories(app_data_path);
    const std::string log_path =
        (std::filesystem::path(app_data_path) / "caninana.log").string();
    log_file_.open(log_path, std::ios::out | std::ios::app);
  } catch (const std::filesystem::filesystem_error& e) {
    // If we can't write to the file, log to stderr as a last resort.
    std::cerr << "FATAL: Could not open log file: " << e.what() << std::endl;
  }
}

SecurityLogger::~SecurityLogger() {
  if (log_file_.is_open()) {
    log_file_.close();
  }
}

void SecurityLogger::Log(LogLevel level, const std::string& component,
                         const std::string& message) {
  // Lock the mutex to ensure writes from different threads are not interleaved.
  std::lock_guard<std::mutex> guard(log_mutex_);
  const std::string formatted_message = "[" + GetTimestamp() + "] [" +
                                        LevelToString(level) + "] [" +
                                        component + "] " + message;

  if (log_file_.is_open()) {
    log_file_ << formatted_message << std::endl;
  } else {
    // Fallback to standard error if the log file is not available.
    std::cerr << formatted_message << std::endl;
  }
}

std::string SecurityLogger::LevelToString(LogLevel level) const {
  switch (level) {
    case LogLevel::INFO:
      return "INFO";
    case LogLevel::WARNING:
      return "WARNING";
    case LogLevel::LOG_ERROR:
      return "ERROR";
    case LogLevel::CRITICAL:
      return "CRITICAL";
  }
  return "UNKNOWN";
}

std::string SecurityLogger::GetTimestamp() const {
  const auto now = std::chrono::system_clock::now();
  const auto in_time_t = std::chrono::system_clock::to_time_t(now);
  std::stringstream ss;
  // Use std::localtime for local time zone conversion.
  ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");
  return ss.str();
}

}  // namespace core
}  // namespace caninana