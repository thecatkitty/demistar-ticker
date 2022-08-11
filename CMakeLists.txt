cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(test_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(PICO_BOARD pico_w)
pico_sdk_init()

include_directories(BEFORE SYSTEM inc)

add_executable(demistar-fw
        src/main.cpp
        src/ws2812.cpp)

target_link_libraries(demistar-fw
        pico_stdlib
        pico_cyw43_arch_lwip_poll)

pico_enable_stdio_usb(demistar-fw 1)
pico_enable_stdio_uart(demistar-fw 1)

# create map/bin/hex file etc.
pico_add_extra_outputs(demistar-fw)
