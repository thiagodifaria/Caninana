#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <sstream>
#include <string>

#include "file_analyzer.h"
#include "file_exception.h"
#include "quarantine_manager.h"
#include "signature_engine.h"
#include "signature_updater.h"

namespace py = pybind11;

PYBIND11_MODULE(caninana_core, m) {
  m.doc() = "Python bindings for the Caninana C++ core engine";

  using namespace caninana::core;

  // --- Exception Bindings ---
  // The base exception is registered first.
  py::register_exception<FileException>(m, "FileError");

  // All other custom exceptions should inherit from the Python `FileError`
  // that we just registered on the module `m`. We do this using m.attr().
  py::register_exception<FileAccessError>(m, "FileAccessError", m.attr("FileError"));
  py::register_exception<DatabaseParseError>(m, "DatabaseParseError", m.attr("FileError"));
  py::register_exception<InitializationError>(m, "InitializationError", m.attr("FileError"));
  py::register_exception<QuarantineError>(m, "QuarantineError", m.attr("FileError"));


  // --- Enum and Struct Bindings ---
  py::enum_<FileType>(m, "FileType")
      .value("EXECUTABLE", FileType::EXECUTABLE)
      .value("ARCHIVE", FileType::ARCHIVE)
      .value("DOCUMENT", FileType::DOCUMENT)
      .value("IMAGE", FileType::IMAGE)
      .value("SCRIPT", FileType::SCRIPT)
      .value("UNKNOWN", FileType::UNKNOWN)
      .value("SUSPICIOUS", FileType::SUSPICIOUS)
      .export_values();

  py::class_<FileInfo>(m, "FileInfo")
      .def(py::init<>())
      .def_readwrite("type", &FileInfo::type)
      .def_readwrite("extension", &FileInfo::extension)
      .def_readwrite("size", &FileInfo::size)
      .def_readwrite("sha256_hash", &FileInfo::sha256_hash);

  py::class_<SignatureEngine::ScanResult>(m, "ScanResult")
      .def(py::init<>())
      .def_readwrite("status", &SignatureEngine::ScanResult::status)
      .def_readwrite("threat_detected",
                     &SignatureEngine::ScanResult::threat_detected)
      .def_readwrite("detected_signatures",
                     &SignatureEngine::ScanResult::detected_signatures)
      .def_readwrite("max_severity",
                     &SignatureEngine::ScanResult::max_severity);

  py::enum_<SignatureEngine::ScanResult::ScanStatus>(m, "ScanStatus")
      .value("COMPLETE", SignatureEngine::ScanResult::ScanStatus::COMPLETE)
      .value("TIMEOUT_ERROR",
             SignatureEngine::ScanResult::ScanStatus::TIMEOUT_ERROR)
      .export_values();

  py::class_<QuarantineEntry>(m, "QuarantineEntry")
      .def(py::init<>())
      .def_readwrite("quarantine_id", &QuarantineEntry::quarantine_id)
      .def_readwrite("original_path", &QuarantineEntry::original_path)
      .def_readwrite("quarantine_date", &QuarantineEntry::quarantine_date)
      .def_readwrite("threat_name", &QuarantineEntry::threat_name);

  // --- Class Bindings ---
  py::class_<FileTypeAnalyzer>(m, "FileTypeAnalyzer")
      .def(py::init<>())
      .def("analyze_file", &FileTypeAnalyzer::AnalyzeFile,
           py::arg("filepath"));

  py::class_<SignatureEngine>(m, "SignatureEngine")
      .def(py::init<>())
      .def("load_signatures", &SignatureEngine::LoadSignatures,
           py::arg("signature_db_path"))
      .def(
          "scan_bytes",
          [](SignatureEngine& self, const py::bytes& file_content,
             const FileInfo& file_info) {
            std::string content_str(file_content);
            std::stringstream stream(content_str);
            return self.Scan(stream, file_info);
          },
          py::arg("file_content"), py::arg("file_info"));

  py::class_<QuarantineManager>(m, "QuarantineManager")
      .def(py::init<const std::string&>(), py::arg("root_path") = "")
      .def("quarantine_file", &QuarantineManager::QuarantineFile,
           py::arg("filepath"), py::arg("threat"))
      .def("restore_file", &QuarantineManager::RestoreFile,
           py::arg("quarantine_id"))
      .def("list_quarantined_files",
           &QuarantineManager::ListQuarantinedFiles);

  py::class_<SignatureUpdater>(m, "SignatureUpdater")
      .def(py::init<const std::string&>(), py::arg("base_url"))
      .def("check_for_updates", &SignatureUpdater::CheckForUpdates,
           py::arg("current_db_path"),
           "Checks for new signatures, returning True if an update was applied.");
}