[![Build Status](https://travis-ci.org/uilianries/conan-libpcap.svg?branch=release/1.8.1)](https://travis-ci.org/uilianries/conan-libpcap) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# An API for capturing network traffic

[Conan.io](https://conan.io) package for [libpcap](https://github.com/the-tcpdump-group/libpcap) project

    The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/libpcap/1.8.1/uilianries/stable).

## Build packages

    Download conan client from [Conan.io](https://conan.io) and run:

        $ python build.py

    If your are in Windows you should run it from a VisualStudio console in order to get "mc.exe" in path.

## Upload packages to server

        $ conan upload libpcap/1.8.1@uilianries/stable --all

## Reuse the packages

### Basic setup

        $ conan install libpcap/1.8.1@uilianries/stable

### Project setup

    If you handle multiple dependencies in your project is better to add a *conanfile.txt*

        [requires]
        libpcap/1.8.1@uilianries/stable

        [options]
        libpcap:shared=True # False

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

### License
[BSD](LICENSE)
