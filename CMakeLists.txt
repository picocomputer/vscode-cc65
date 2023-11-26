cmake_minimum_required(VERSION 3.13)

project(MY-RP6502-PROJECT C ASM)

add_subdirectory(tools)

add_executable(hello)
rp6502_executable(hello)
target_sources(hello PRIVATE
    src/main.c
)
