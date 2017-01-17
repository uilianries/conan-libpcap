from conans.model.conan_file import ConanFile
from conans import CMake
import os


class TestPcapConan(ConanFile):
    name = "TestPcap"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "libpcap/1.8@uilianries/testing"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.a", dst="bin", src="bin")
        
    def test(self):
        self.run("cd bin && .%sconan-libpcap-test" % os.sep)
