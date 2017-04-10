"""Validation for Pcap library package

"""
from os import getenv
from conans import CMake
from conans import ConanFile


class TestPcapConan(ConanFile):
    """Build test with libpcap package
    """
    target = "libpcap"
    name = "%s-test" % target
    version = "1.8.1"
    author = "Uilian Ries <uilianries@gmail.com>"
    license = "BSD"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    channel = getenv("CONAN_CHANNEL", "testing")
    user = getenv("CONAN_USERNAME", "uilianries")
    requires = "%s/%s@%s/%s" % (target, version, user, channel)

    def build(self):
        cmake = CMake(self.settings)
        cmake.configure(self, source_dir=self.conanfile_directory, build_dir="./")
        cmake.build(self)

    def imports(self):
        self.copy(pattern="*.so*", dst="bin", src="lib")

    def test(self):
        cmake = CMake(self.settings)
        cmake.configure(self, source_dir=self.conanfile_directory, build_dir="./")
        cmake.build(self, target="test")
