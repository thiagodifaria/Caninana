#ifndef CANINANA_CORE_INCLUDE_FILE_ANALYZER_H_
#define CANINANA_CORE_INCLUDE_FILE_ANALYZER_H_

#include <cstdint>
#include <iosfwd>
#include <string>
#include <vector>

namespace caninana {
namespace core {

/**
 * @brief Represents the determined type of a file based on its content.
 */
enum class FileType {
  EXECUTABLE, ///< A platform-native executable (e.g., PE for Windows).
  ARCHIVE,    ///< A compressed archive file (e.g., ZIP).
  DOCUMENT,   ///< A document file (e.g., PDF).
  IMAGE,      ///< An image file.
  SCRIPT,     ///< A script file (e.g., Python, Bash).
  UNKNOWN,    ///< The file type could not be determined or is not supported.
  SUSPICIOUS, ///< The file has characteristics that warrant deeper inspection.
};  // FIX: The semicolon at the end of the enum definition was missing.

/**
 * @brief Holds the results of a file analysis operation.
 *
 * This struct aggregates essential metadata about a file, which is used by the
 * main scanning engine to make informed decisions.
 */
struct FileInfo {
  FileType type{FileType::UNKNOWN}; ///< The identified type of the file.
  std::string extension;             ///< The file's extension (e.g., ".exe").
  uint64_t size{0};                  ///< The total size of the file in bytes.
  std::string sha256_hash;           ///< The SHA256 hash of the file's contents.
};

/**
 * @class FileTypeAnalyzer
 * @brief Performs initial static analysis on a file using a streaming approach.
 *
 * This class is responsible for reading a file and extracting its fundamental
 * properties: type, size, and a cryptographic hash. The implementation uses
 * file streams to ensure a small, constant memory footprint, regardless of the
 * file size. This is critical for performance and scalability in a real-world
 * antivirus engine.
 */
class FileTypeAnalyzer {
 public:
  /**
   * @brief Analyzes a file to determine its type, size, and SHA256 hash.
   *
   * This is the primary entry point for file analysis. It processes the file
   * in chunks to maintain a low memory profile. It inspects the initial bytes
   * to identify the file type and streams the entire file to compute the SHA256
   * hash.
   *
   * @param filepath The full path to the file to be analyzed.
   * @return A FileInfo struct containing the analysis results. If the file
   * cannot be opened or read, the struct will contain default values,
   * including a FileType of UNKNOWN.
   */
  FileInfo AnalyzeFile(const std::string& filepath);

 private:
  /**
   * @brief Calculates the SHA256 hash of a file stream.
   *
   * This method reads the stream in chunks, updating the hash context with each
   * chunk. This allows for hashing files of any size with minimal memory usage.
   *
   * @param file_stream An input stream positioned at the beginning of the file.
   * @return A lowercase hexadecimal string representing the SHA256 hash.
   */
  std::string CalculateSha256(std::istream& file_stream) const;

  /**
   * @brief Identifies the file type based on an initial chunk of its content.
   *
   * @param initial_buffer A buffer containing the first few bytes of the file.
   * @return The identified FileType based on magic numbers.
   */
  FileType IdentifyFileType(const std::vector<char>& initial_buffer) const;
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_FILE_ANALYZER_H_