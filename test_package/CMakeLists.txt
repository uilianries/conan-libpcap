################################################################################
# CMake receipt for libpcap test
#
# Copyright 2017 Uilian Ries <uilianries@gmail.com>
################################################################################
PROJECT(conan-libpcap-test)
cmake_minimum_required(VERSION 2.8)

# Import Conan package #########################################################
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

# Build test ###################################################################
ADD_EXECUTABLE(${CMAKE_PROJECT_NAME} main.c)
TARGET_LINK_LIBRARIES(${CMAKE_PROJECT_NAME} ${CONAN_LIBS})
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY C_STANDARD 99)

# Execute test #################################################################
enable_testing()
add_test(DeviceInfo bin/${CMAKE_PROJECT_NAME})
