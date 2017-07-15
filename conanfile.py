"""Conan.io recipe for pcap library
"""
from os import unlink
from os.path import join
from tempfile import mkdtemp
from platform import machine
from conans import ConanFile
from conans import AutoToolsBuildEnvironment
from conans.tools import SystemPackageTool
from conans.tools import download
from conans.tools import unzip
from conans.tools import chdir
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
    license = "https://github.com/the-tcpdump-group/libpcap/blob/master/LICENSE"
    default_options = "shared=True", "enable_dbus=True", "enable_bluetooth=True", "enable_usb=True", "enable_packet_ring=True"
    libpcap_dir = "%s-%s-%s" % (name, name, version)
    install_dir = mkdtemp(suffix=name)

    def build_requirements(self):
        if self.settings.os == "Linux":
            package_tool = SystemPackageTool()
            package_tool.install(packages="bison flex")

    def _is_amd64_to_i386(self):
        return self.settings.arch == "x86" and machine() == "x86_64"

    def system_requirements(self):
        if self.settings.os == "Linux":
            arch = ":i386" if self._is_amd64_to_i386() else ""
            package_list = []
            if self.options.enable_dbus:
                package_list.extend(["libdbus-glib-1-dev%s" % arch, "libdbus-1-dev"])
            if self.options.enable_bluetooth:
                package_list.append("libbluetooth-dev%s" % arch)
            if self.options.enable_usb:
                package_list.append("libusb-1.0-0-dev%s" % arch)
            if self.options.enable_packet_ring:
                package_list.append("libnl-genl-3-dev%s" % arch)
            if package_list:
                package_tool = SystemPackageTool()
                package_tool.install(packages=" ".join(package_list))

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tar_name = "%s-%s.tar.gz" % (self.name, self.version)
        url = "https://github.com/the-tcpdump-group/libpcap/archive/%s" % tar_name
        download(url, tar_name)
        check_md5(tar_name, "4a70f59c943b21340deca4affe63ea4c")
        unzip(tar_name)
        unlink(tar_name)

    def build(self):
        with chdir(self.libpcap_dir):
            env_build = AutoToolsBuildEnvironment(self)
            configure_args = ["--prefix=%s" % self.install_dir]
            configure_args.append("--enable-shared" if self.options.shared else "--disable-shared")
            configure_args.append("--enable-dbus" if self.options.enable_dbus else "--disable-dbus")
            configure_args.append("--enable-bluetooth" if self.options.enable_bluetooth else "--disable-bluetooth")
            configure_args.append("--enable-usb" if self.options.enable_usb else "--disable-usb")
            configure_args.append("--enable-packet-ring" if self.options.enable_packet_ring else "--disable-packet_ring")
            env_build.fpic = True
            env_build.configure(args=configure_args)
            env_build.make(args=["all"])
            env_build.make(args=["install"])

    def package(self):
        self.copy("LICENSE", src=self.libpcap_dir, dst=".")
        self.copy(pattern="*", dst="bin", src=join(self.install_dir, "bin"))
        self.copy(pattern="*.h", dst="include", src=join(self.install_dir, "include"))
        self.copy(pattern="*.so*", dst="lib", src=join(self.install_dir, "lib"), keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=join(self.install_dir, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["pcap"]
        if self.settings.os == "Linux":
            if self.options.enable_dbus:
                self.cpp_info.libs.append("dbus-glib-1")
                self.cpp_info.libs.append("dbus-1")
            if self.options.enable_bluetooth:
                self.cpp_info.libs.append("bluetooth")
            if self.options.enable_usb:
                self.cpp_info.libs.append("usb-1.0")
            if self.options.enable_packet_ring:
                self.cpp_info.libs.append("nl-genl-3")
                self.cpp_info.libs.append("nl-3")
