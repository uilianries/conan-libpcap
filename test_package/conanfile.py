"""Validation for Pcap library package

"""
from os import getenv
from conans import CMake
from conans import ConanFile


class TestPcapConan(ConanFile):
    """Build test with libpcap package
    """
    author = "Uilian Ries <uilianries@gmail.com>"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    channel = getenv("CONAN_CHANNEL", "testing")
    username = getenv("CONAN_USERNAME", "uilianries")
    requires = "libpcap/1.8.1@%s/%s" % (username, channel)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.so*", dst="bin", src="lib")

    def test(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.test()
