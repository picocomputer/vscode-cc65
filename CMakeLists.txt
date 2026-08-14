cmake_minimum_required(VERSION 3.21)

# Fetches tools/ on the first configure. See tools/CMakeLists.txt.
include(${CMAKE_CURRENT_LIST_DIR}/tools/CMakeLists.txt)

# Pick a compiler: uncomment one line, or select a CMake preset.
#set(CC65_TARGET_SYSTEM rp6502)
#set(LLVM_MOS_PLATFORM rp6502)

if(DEFINED CC65_TARGET_SYSTEM)
    find_package(cc65 REQUIRED)
elseif(DEFINED LLVM_MOS_PLATFORM)
    find_package(llvm-mos-sdk REQUIRED)
else()
    rp6502_require_toolchain()
endif()

project(MY-RP6502-PROJECT C ASM) # llvm-mos also does C++; add CXX here

add_executable(hello)
rp6502_asset(hello help src/help.txt)
rp6502_executable(hello DATA default RESET default)
target_sources(hello PRIVATE
    src/main.c
)
