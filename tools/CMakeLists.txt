# Fetches the RP6502 project tools from picocomputer/rp6502, then
# replaces itself with the full version. The tools are ordinary
# files in your repository after that; commit them.
#
# Update with:  cmake -P tools/CMakeLists.txt

cmake_minimum_required(VERSION 3.21)

# TODO: back to main once the centraltools work is tested.
set(RP6502_TOOLS_REPO "picocomputer/rp6502")
set(RP6502_TOOLS_REF "centraltools")
set(RP6502_TOOLS_FILES cc65-config.cmake cc65.cmake rp6502.py CMakeLists.txt)

set(RP6502_TOOLS_DIR "${CMAKE_CURRENT_LIST_DIR}")

foreach(name IN LISTS RP6502_TOOLS_FILES)
    set(url "https://raw.githubusercontent.com/${RP6502_TOOLS_REPO}/${RP6502_TOOLS_REF}/tools/${name}")
    set(out "${RP6502_TOOLS_DIR}/${name}")
    message(STATUS "Fetching tools/${name}")
    file(DOWNLOAD "${url}" "${out}.tmp"
        STATUS status
        TLS_VERIFY ON
        INACTIVITY_TIMEOUT 30
    )
    list(GET status 0 code)
    list(GET status 1 text)
    file(SIZE "${out}.tmp" size)
    if(NOT code EQUAL 0 OR size EQUAL 0)
        file(REMOVE "${out}.tmp")
        message(FATAL_ERROR "Cannot fetch ${url}\n${text}")
    endif()
    file(RENAME "${out}.tmp" "${out}")
endforeach()

set(RP6502_TOOLS_FETCHED TRUE)
set(RP6502_TOOLS_RELOADED TRUE)
include("${RP6502_TOOLS_DIR}/CMakeLists.txt")
