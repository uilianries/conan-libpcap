"""Pcap library package for conan.io

"""
from tempfile import mkdtemp
from conans import ConanFile


class PcapConan(ConanFile):
    """Build libpcap

    This package is supported in linux
    """
    name = "libpcap"
    version = "1.8"
    url = "http://github.com/uilianries/conan-libpcap"
    author = "Uilian Ries <uilianries@gmail.com>"
    settings = {"os": ["Linux"]}
    generators = "cmake", "txt"
    description = "Pcap library package for conan.io"
    license = "https://raw.githubusercontent.com/the-tcpdump-group/libpcap/master/LICENSE"
    install_dir = mkdtemp()

    def source(self):
        self.run(
            "git clone --branch libpcap-%s https://github.com/the-tcpdump-group/libpcap.git"
            % self.version)

    def build(self):
        self.run("cd libpcap && ./configure --prefix=%s && make install" %
                 self.install_dir)

    def package(self):
        self.copy("*", src=self.install_dir)

    def package_info(self):
        self.cpp_info.libs = ["pcap"]
