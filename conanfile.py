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
        cmake = CMake(self.settings)
        options_pcap = "-DBUILD_SHARED_LIBS=OFF"
        if self.settings.os == "Windows":
            options_pcap += " -DUSE_STATIC_RT=OFF"
        conf_command = 'cd libpcap && cmake . %s %s' % (cmake.command_line, options_pcap)
        self.output.warn(conf_command)
        self.run(conf_command)
        self.run("cd libpcap && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="libpcap")
        self.copy("*.a", dst="lib", src="libpcap")

    def package_info(self):
        self.cpp_info.libs = ["pcap"]
