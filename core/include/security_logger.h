#ifndef CANINANA_CORE_INCLUDE_SECURITY_LOGGER_H_
#define CANINANA_CORE_INCLUDE_SECURITY_LOGGER_H_

#include <fstream>
#include <mutex>
#include <string>

namespace caninana {
namespace core {

/**
 * @class SecurityLogger
 * @brief A thread-safe singleton for logging security and operational events.
 *
 * Provides a centralized logging facility for the entire core engine, writing
 * timestamped messages to a persistent file. This is critical for auditing,
 * forensics, and debugging.
 */
class SecurityLogger {
 public:
  /**
   * @enum LogLevel
   * @brief Defines the severity of a log message.
   */
  enum class LogLevel { INFO, WARNING, LOG_ERROR, CRITICAL };

  /**
   * @brief Retrieves the singleton instance of the logger.
   * @return A reference to the single SecurityLogger instance.
   */
  static SecurityLogger& GetInstance();

  /**
   * @brief Writes a formatted message to the log file.
   * @param level The severity level of the event.
   * @param component The name of the component logging the event (e.g.,
   * "SignatureEngine").
   * @param message The detailed log message.
   */
  void Log(LogLevel level, const std::string& component,
           const std::string& message);

  // Delete copy constructor and assignment operator to enforce singleton
  // pattern.
  SecurityLogger(const SecurityLogger&) = delete;
  void operator=(const SecurityLogger&) = delete;

 private:
  // Private constructor and destructor for the singleton pattern.
  SecurityLogger();
  ~SecurityLogger();

  std::string LevelToString(LogLevel level) const;
  std::string GetTimestamp() const;

  std::ofstream log_file_;
  std::mutex log_mutex_;
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_SECURITY_LOGGER_H_