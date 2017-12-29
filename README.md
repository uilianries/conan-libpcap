[![Build Status](https://travis-ci.org/bincrafters/conan-libpcap.svg?branch=release/1.8.1)](https://travis-ci.org/bincrafters/conan-libpcap) [![badge](https://img.shields.io/badge/conan.io-libpcap%2F1.8.1-green.svg?logo=data:image/png;base64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAA1VBMVEUAAABhlctjlstkl8tlmMtlmMxlmcxmmcxnmsxpnMxpnM1qnc1sn85voM91oM11oc1xotB2oc56pNF6pNJ2ptJ8ptJ8ptN9ptN8p9N5qNJ9p9N9p9R8qtOBqdSAqtOAqtR%2BrNSCrNJ/rdWDrNWCsNWCsNaJs9eLs9iRvNuVvdyVv9yXwd2Zwt6axN6dxt%2Bfx%2BChyeGiyuGjyuCjyuGly%2BGlzOKmzOGozuKoz%2BKqz%2BOq0OOv1OWw1OWw1eWx1eWy1uay1%2Baz1%2Baz1%2Bez2Oe02Oe12ee22ujUGwH3AAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfgBQkREyOxFIh/AAAAiklEQVQI12NgAAMbOwY4sLZ2NtQ1coVKWNvoc/Eq8XDr2wB5Ig62ekza9vaOqpK2TpoMzOxaFtwqZua2Bm4makIM7OzMAjoaCqYuxooSUqJALjs7o4yVpbowvzSUy87KqSwmxQfnsrPISyFzWeWAXCkpMaBVIC4bmCsOdgiUKwh3JojLgAQ4ZCE0AMm2D29tZwe6AAAAAElFTkSuQmCC)](https://bintray.com/bincrafters/conan/libpcap%3Abincrafters)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Download](https://api.bintray.com/packages/bincrafters/public-conan/libpcap%3Abincrafters/images/download.svg?version=1.8.1%3Astable)](https://bintray.com/bincrafters/public-conan/libpcap%3Abincrafters/1.8.1%3Astable/link)

## PCAP library is an API for capturing network traffic

![conan-libpcap](logo.png)

[Conan.io](https://conan.io) package for [libpcap](https://github.com/the-tcpdump-group/libpcap) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/libpcap%3Abincrafters).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

If your are in Windows you should run it from a VisualStudio console in order to get "mc.exe" in path.

## Upload packages to server

    $ conan upload libpcap/1.8.1@bincrafters/stable --all

## Reuse the packages

### Basic setup

    $ conan install libpcap/1.8.1@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    libpcap/1.8.1@bincrafters/stable

    [options]
    libpcap:shared=True # False

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

### License
[MIT](LICENSE.md)
