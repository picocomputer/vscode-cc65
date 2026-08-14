# Fetches the RP6502 project tools from picocomputer/rp6502, then
# replaces itself with the full version. The tools are ordinary
# files in your repository after that; commit them.
#
# Update with:  cmake -P tools/CMakeLists.txt

cmake_minimum_required(VERSION 3.21)

# TODO: back to main once the centraltools work is tested.
set(RP6502_TOOLS_REPO "picocomputer/rp6502")
set(RP6502_TOOLS_REF "centraltools")

set(RP6502_TOOLS_DIR "${CMAKE_CURRENT_LIST_DIR}")

# Rename over the target, so a dead network leaves the working tool in place.
function(rp6502_fetch_tool name hash)
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
    # Checked here rather than with EXPECTED_HASH, which reports a mismatch
    # without stopping: the rest of the manifest still came down, the partial
    # file stayed, and this message never ran.
    if(hash)
        file(SHA256 "${out}.tmp" got)
        string(TOLOWER "${hash}" hash)
        if(NOT got STREQUAL hash)
            file(REMOVE "${out}.tmp")
            message(FATAL_ERROR
                "Wrong contents for tools/${name}\n"
                "expected ${hash}\n"
                "     got ${got}")
        endif()
    endif()
    file(RENAME "${out}.tmp" "${out}")
endfunction()

# What to fetch, and what it should hash to, comes from the server. This file
# is older than whatever the tool set has become and must not assume.
rp6502_fetch_tool(manifest.txt "")
file(STRINGS "${RP6502_TOOLS_DIR}/manifest.txt" lines)
file(REMOVE "${RP6502_TOOLS_DIR}/manifest.txt")
set(fetched FALSE)
foreach(line IN LISTS lines)
    if(line MATCHES "^([0-9a-fA-F]+)[ \t]+(.+)$")
        rp6502_fetch_tool("${CMAKE_MATCH_2}" "${CMAKE_MATCH_1}")
        set(fetched TRUE)
    endif()
endforeach()
if(NOT fetched)
    message(FATAL_ERROR "tools/manifest.txt lists nothing to fetch.")
endif()

set(RP6502_TOOLS_FETCHED TRUE)
set(RP6502_TOOLS_RELOADED TRUE)
include("${RP6502_TOOLS_DIR}/CMakeLists.txt")
