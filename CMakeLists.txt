# Root CMakeLists.txt for the Caninana Project (vcpkg version - FINAL v2)
cmake_minimum_required(VERSION 3.18)
project(Caninana LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Set Global Output Directories (More Robust) ---
# This tells ALL targets in the project where to put their output files.
# This is a more forceful way to ensure the .pyd file ends up in the right place.
foreach(CONFIG ${CMAKE_CONFIGURATION_TYPES})
    string(TOUPPER ${CONFIG} CONFIG_UPPER)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${CONFIG_UPPER} "${CMAKE_SOURCE_DIR}/ui")
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_${CONFIG_UPPER} "${CMAKE_SOURCE_DIR}/ui")
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_${CONFIG_UPPER} "${CMAKE_SOURCE_DIR}/ui")
endforeach()


# --- Find Dependencies (vcpkg makes this easy) ---
find_package(nlohmann_json CONFIG REQUIRED)
find_package(OpenSSL CONFIG REQUIRED)
find_package(Python 3.7 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG REQUIRED)


# --- Core Library Subdirectory ---
add_subdirectory(core)


# --- Python Module Definition ---
pybind11_add_module(caninana_core
    core/src/bindings.cpp
)

# Link our Python module against our C++ library.
target_link_libraries(caninana_core PRIVATE CaninanaCore)