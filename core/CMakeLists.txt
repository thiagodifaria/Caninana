# core/CMakeLists.txt for the Caninana Core Library

# Define a library target from our source files.
# This encapsulates all our core logic.
add_library(CaninanaCore
    src/file_analyzer.cpp
    src/signature_engine.cpp
    src/performance_monitor.cpp
    src/quarantine_manager.cpp
    src/security_logger.cpp
    src/signature_updater.cpp
)

# Make the 'include' directory available to any other target
# that links against CaninanaCore. This is good practice for modularity.
target_include_directories(CaninanaCore
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Find all required dependencies via vcpkg.
find_package(unofficial-libmagic REQUIRED)
# FIX: Use the CONFIG keyword to be explicit about expecting a CMake package
# configuration file, which is the modern and preferred method.
find_package(cpr CONFIG REQUIRED)

# Link all necessary dependencies to the core library.
target_link_libraries(CaninanaCore
    PRIVATE
        # For SHA256 hashing
        OpenSSL::SSL
        OpenSSL::Crypto

        # For JSON parsing
        nlohmann_json::nlohmann_json

        # For robust, production-grade file type identification
        unofficial::libmagic::libmagic

        # For HTTP requests
        cpr::cpr
)