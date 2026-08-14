# The stub that goes and gets the RP6502 project tools.
#
# This is the only tools file a new project starts with. The first configure
# replaces it with the full version from picocomputer/rp6502, which carries
# the same fetch loop plus the rp6502_* build commands. From then on the tools
# are ordinary files in your repository: commit them, and an update arrives as
# a diff you can read.
#
# Update from the command line with:
#
#   cmake -P tools/CMakeLists.txt

cmake_minimum_required(VERSION 3.21)

# TODO: back to main once the centraltools work is tested.
set(RP6502_TOOLS_REPO "picocomputer/rp6502")
set(RP6502_TOOLS_REF "centraltools")
set(RP6502_TOOLS_FILES CMakeLists.txt cc65-config.cmake cc65.cmake rp6502.py)

set(RP6502_TOOLS_DIR "${CMAKE_CURRENT_LIST_DIR}")

# Everything, unconditionally: this file exists, so a fetch-what-is-missing
# loop would never replace the one file that has to be replaced.
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

# Hand off to what just landed. It defines the rp6502_* commands this project
# is about to call, and runs the hooks that bring an older project's config
# files up to date.
set(RP6502_TOOLS_FETCHED TRUE)
set(RP6502_TOOLS_RELOADED TRUE)
include("${RP6502_TOOLS_DIR}/CMakeLists.txt")
