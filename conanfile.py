"""Conan.io recipe for pcap library
"""
from os import unlink
from os.path import join
from tempfile import mkdtemp
from conans import ConanFile
from conans import AutoToolsBuildEnvironment
from conans.tools import download
from conans.tools import unzip
from conans.tools import chdir
from conans.tools import environment_append
from conans.tools import check_md5


class LibPcapConan(ConanFile):
    """Donwload pcap library, build and create package
    """
    name = "libpcap"
    version = "1.8.1"
    generators = "cmake", "txt"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "enable_dbus": [True, False],
        "enable_bluetooth": [True, False],
        "enable_usb": [True, False],
        "enable_packet_ring": [True, False]
    }
    url = "http://github.com/uilianries/conan-libpcap"
    author = "Uilian Ries <uilianries@gmail.com>"
    description = "An API for capturing network traffic"
    license = "BSD"
    default_options = "shared=False", "enable_dbus=False", "enable_bluetooth=False", "enable_usb=False", "enable_packet_ring=False"
    install_dir = mkdtemp(suffix=name)

    def source(self):
        tar_name = "%s-%s.tar.gz" % (self.name, self.version)
        url = "https://github.com/the-tcpdump-group/libpcap/archive/%s" % tar_name
        download(url, tar_name)
        check_md5(tar_name, "4a70f59c943b21340deca4affe63ea4c")
        unzip(tar_name)
        unlink(tar_name)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.shared
        with environment_append(env_build.vars):
            with chdir("%s-%s-%s" % (self.name, self.name, self.version)):
                options = "--enable-shared" if self.options.shared else "--disable-shared"
                options += " --enable-dbus" if self.options.enable_dbus else " --disable-dbus"
                options += " --enable-bluetooth" if self.options.enable_bluetooth else " --disable-bluetooth"
                options += " --enable-usb" if self.options.enable_usb else " --disable-usb"
                options += " --enable-packet-ring" if self.options.enable_packet_ring else " --disable-packet_ring"
                self.run("./configure --prefix=%s %s" % (self.install_dir, options))
                self.run("make")
                self.run("make install")

    def package(self):
        self.copy(pattern="*.h", dst="include", src=join(self.install_dir, "include"))
        self.copy(pattern="*.a", dst="lib", src=join(self.install_dir, "lib"), keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=join(self.install_dir, "lib"), keep_path=False)
        self.copy(pattern="*", dst="bin", src=join(self.install_dir, "bin"))

    def package_info(self):
        self.cpp_info.libs = ["pcap"]
