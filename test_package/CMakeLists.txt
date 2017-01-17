PROJECT(conan-libpcap-test)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(${CMAKE_PROJECT_NAME} main.cpp)
TARGET_LINK_LIBRARIES(${CMAKE_PROJECT_NAME} ${CONAN_LIBS})
