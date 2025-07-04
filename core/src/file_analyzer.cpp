#include "file_analyzer.h"

#include <openssl/sha.h>
#include <magic.h>

#include <filesystem>
#include <fstream>
#include <iomanip>
#include <istream>
#include <sstream>

#include "file_exception.h"
#include "security_logger.h"

namespace caninana {
namespace core {

namespace {
constexpr size_t kBufferSize = 8192;
}

FileInfo FileTypeAnalyzer::AnalyzeFile(const std::string& filepath) {
  FileInfo info;
  std::error_code ec;
  const std::filesystem::path path(filepath);

  info.size = std::filesystem::file_size(path, ec);
  if (ec) {
    throw FileAccessError("Failed to get file size for '" + filepath +
                          "': " + ec.message());
  }

  info.extension = path.extension().string();

  if (info.size == 0) {
    info.sha256_hash =
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    return info;
  }

  std::ifstream file(filepath, std::ios::binary);
  if (!file.is_open()) {
    throw FileAccessError("Failed to open file for analysis: " + filepath);
  }

  std::vector<char> initial_buffer(kBufferSize);
  file.read(initial_buffer.data(), kBufferSize);
  initial_buffer.resize(file.gcount());
  info.type = IdentifyFileType(initial_buffer);

  file.clear();
  file.seekg(0, std::ios::beg);
  info.sha256_hash = CalculateSha256(file);

  return info;
}

FileType FileTypeAnalyzer::IdentifyFileType(
    const std::vector<char>& initial_buffer) const {
  if (initial_buffer.empty()) {
    return FileType::UNKNOWN;
  }
  magic_t magic_cookie = magic_open(MAGIC_MIME_TYPE | MAGIC_ERROR);
  if (magic_cookie == nullptr) {
    return FileType::UNKNOWN;
  }
  if (magic_load(magic_cookie, nullptr) != 0) {
    magic_close(magic_cookie);
    return FileType::UNKNOWN;
  }
  const char* description =
      magic_buffer(magic_cookie, initial_buffer.data(), initial_buffer.size());
  if (description == nullptr) {
    magic_close(magic_cookie);
    return FileType::UNKNOWN;
  }
  std::string desc_str(description);
  magic_close(magic_cookie);

  if (desc_str.find("executable") != std::string::npos ||
      desc_str.find("x-dosexec") != std::string::npos ||
      desc_str.find("x-pie-executable") != std::string::npos ||
      desc_str.find("x-elf") != std::string::npos) {
    return FileType::EXECUTABLE;
  }
  if (desc_str.find("x-python") != std::string::npos ||
      desc_str.find("x-shellscript") != std::string::npos) {
    return FileType::SCRIPT;
  }
  if (desc_str.find("pdf") != std::string::npos ||
      desc_str.find("word") != std::string::npos ||
      desc_str.find("rtf") != std::string::npos) {
    return FileType::DOCUMENT;
  }
  if (desc_str.find("zip") != std::string::npos ||
      desc_str.find("rar") != std::string::npos ||
      desc_str.find("x-7z-compressed") != std::string::npos ||
      desc_str.find("x-tar") != std::string::npos) {
    return FileType::ARCHIVE;
  }
  if (desc_str.find("image/") == 0) {
    return FileType::IMAGE;
  }
  return FileType::UNKNOWN;
}

std::string FileTypeAnalyzer::CalculateSha256(
    std::istream& file_stream) const {
  unsigned char hash[SHA256_DIGEST_LENGTH];
  std::vector<char> buffer(kBufferSize);
  SHA256_CTX sha256_context;
  if (!SHA256_Init(&sha256_context)) {
    return "";
  }
  while (file_stream) {
    file_stream.read(buffer.data(), kBufferSize);
    const std::streamsize bytes_read = file_stream.gcount();
    if (bytes_read > 0) {
      SHA256_Update(&sha256_context, buffer.data(),
                    static_cast<size_t>(bytes_read));
    }
  }
  if (!SHA256_Final(hash, &sha256_context)) {
    return "";
  }
  std::stringstream ss;
  ss << std::hex << std::setfill('0');
  for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
    ss << std::setw(2) << static_cast<unsigned int>(hash[i]);
  }
  return ss.str();
}

}  // namespace core
}  // namespace caninana