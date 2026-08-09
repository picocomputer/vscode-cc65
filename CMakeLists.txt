cmake_minimum_required(VERSION 3.20)

set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_LIST_DIR}/tools/rp6502.cmake"
    CACHE FILEPATH "CMake toolchain file")

project(MY-RP6502-PROJECT C ASM)

add_subdirectory(tools)

add_executable(hello)
rp6502_asset(hello help src/help.txt)
rp6502_executable(hello DATA 0x200 RESET 0x200)
target_sources(hello PRIVATE
    src/main.c
)
