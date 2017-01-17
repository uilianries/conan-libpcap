from conans import ConanFile, CMake

class PcapConan(ConanFile):
    name = "libpcap"
    version = "1.8"
    url="http://github.com/uilianries/conan-libpcap"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "txt"
	description = "Pcap library package for conan.io"
    license = "MIT"

    def source(self):
        self.run("git clone --branch libpcap-1.8 https://github.com/the-tcpdump-group/libpcap.git")

    def build(self):
        self.run("%s/libpcap/configure" % self.conanfile_directory)
        self.run("make -C %s" % self.conanfile_directory)

    def package(self):
        self.copy("*.h", dst="include", src="libpcap")
        self.copy("*.a", dst="lib")

    def package_info(self):
        self.cpp_info.libs = ["pcap"]
