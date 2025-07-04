#ifndef CANINANA_CORE_INCLUDE_FILE_EXCEPTION_H_
#define CANINANA_CORE_INCLUDE_FILE_EXCEPTION_H_

#include <stdexcept>
#include <string>

namespace caninana {
namespace core {

/**
 * @brief Base class for all exceptions thrown by the Caninana core engine.
 *
 * Inherits from std::runtime_error to be compatible with standard C++
 * exception handling.
 */
class FileException : public std::runtime_error {
 public:
  explicit FileException(const std::string& message)
      : std::runtime_error(message) {}
};

/**
 * @brief Thrown when a file or directory cannot be accessed due to I/O or
 * permission issues.
 */
class FileAccessError : public FileException {
 public:
  explicit FileAccessError(const std::string& message)
      : FileException(message) {}
};

/**
 * @brief Thrown when a database or configuration file is malformed and cannot
 * be parsed.
 */
class DatabaseParseError : public FileException {
 public:
  explicit DatabaseParseError(const std::string& message)
      : FileException(message) {}
};

/**
 * @brief Thrown when a core component fails to initialize correctly.
 */
class InitializationError : public FileException {
 public:
  explicit InitializationError(const std::string& message)
      : FileException(message) {}
};

/**
 * @brief Thrown for errors specific to the quarantine process, such as a
 * missing file or a failed metadata update.
 */
class QuarantineError : public FileException {
 public:
  explicit QuarantineError(const std::string& message)
      : FileException(message) {}
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_FILE_EXCEPTION_H_