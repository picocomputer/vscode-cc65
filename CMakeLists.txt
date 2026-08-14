cmake_minimum_required(VERSION 3.21)

include(${CMAKE_CURRENT_LIST_DIR}/tools/CMakeLists.txt)

project(MY-RP6502-PROJECT C CXX ASM)

add_executable(hello)
rp6502_asset(hello help src/help.txt)
rp6502_executable(hello DATA default RESET default)
target_sources(hello PRIVATE
    src/main.c
)
