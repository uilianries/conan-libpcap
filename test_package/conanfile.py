"""Validation for Pcap library package

"""
import os
from conans.model.conan_file import ConanFile
from conans import CMake

USERNAME = os.getenv("CONAN_USERNAME", "uilianries")
CHANNEL = os.getenv("CONAN_CHANNEL", "testing")


class TestPcapConan(ConanFile):
    """Build test with libpcap package

    This test list all network devices
    """
    name = "TestPcap"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "libpcap/1.8@%s/%s" % (USERNAME, CHANNEL)

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake %s %s' %
                 (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.a", dst="lib", src="lib")
        self.copy(pattern="*so", dst="bin", src="lib")
        self.copy(pattern="*", dst="bin", src="bin")

    def test(self):
        self.run("cmake --build . --target test")
