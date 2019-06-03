"""Conan.io recipe for pcap library
"""
from conans import AutoToolsBuildEnvironment, tools, ConanFile


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
        "enable_packet_ring": [True, False],
        "disable_universal": [True, False]
    }
    url = "http://github.com/bincrafters/conan-libpcap"
    homepage = "https://github.com/the-tcpdump-group/libpcap"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "libpcap is an API for capturing network traffic"
    license = "https://github.com/the-tcpdump-group/libpcap/blob/master/LICENSE"
    default_options = "shared=False", "enable_dbus=False", "enable_bluetooth=False", "enable_usb=False", "enable_packet_ring=False", "disable_universal=False"
    exports = ["LICENSE.md"]
    libpcap_dir = "%s-%s-%s" % (name, name, version)

    def requirements(self):
        if self.options.enable_usb:
            self.requires("libusb/1.0.21@bincrafters/stable")

    def build_requirements(self):
        if self.settings.os == "Linux":
            if not tools.which("bison"):
                self.build_requires("bison_installer/3.3.2@bincrafters/stable")
            if not tools.which("flex"):
                self.build_requires("flex_installer/2.6.4@bincrafters/stable")

    def _is_amd64_to_i386(self):
        return self.settings.arch == "x86" and tools.detected_architecture() == "x86_64"

    def system_requirements(self):
        if self.settings.os == "Linux":
            arch = ":i386" if self._is_amd64_to_i386() else ""
            package_list = []
            if self.options.enable_dbus:
                package_list.extend(["libdbus-glib-1-dev%s" % arch, "libdbus-1-dev"])
            if self.options.enable_bluetooth:
                package_list.append("libbluetooth-dev%s" % arch)
            if self.options.enable_packet_ring:
                package_list.append("libnl-genl-3-dev%s" % arch)
            if package_list:
                package_tool = tools.SystemPackageTool()
                package_tool.install(packages=" ".join(package_list))

    def source(self):
        tools.get("https://github.com/the-tcpdump-group/libpcap/archive/libpcap-%s.tar.gz" % self.version)

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows":
            raise Exception("For Windows use winpcap/4.1.2@bincrafters/stable")

    def build(self):
        with tools.chdir(self.libpcap_dir):
            env_build = AutoToolsBuildEnvironment(self)
            configure_args = ["--prefix=%s" % self.package_folder]
            configure_args.append("--enable-shared" if self.options.shared else "--disable-shared")
            configure_args.append("--disable-universal" if not self.options.disable_universal else "")
            configure_args.append("--enable-dbus" if self.options.enable_dbus else "--disable-dbus")
            configure_args.append("--enable-bluetooth" if self.options.enable_bluetooth else "--disable-bluetooth")
            configure_args.append("--enable-usb" if self.options.enable_usb else "--disable-usb")
            configure_args.append("--enable-packet-ring" if self.options.enable_packet_ring else "--disable-packet-ring")
            if not self.options.enable_packet_ring:
                configure_args.append("--without-libnl")
            if tools.cross_building(self.settings):
                target_os = "linux" if self.settings.os == "Linux" else "null"
                configure_args.append("--with-pcap=%s" % target_os)
            elif "arm" in self.settings.arch and self.settings.os == "Linux":
                configure_args.append("--host=arm-linux")
            env_build.fpic = True
            env_build.configure(args=configure_args)
            env_build.make(args=["all"])
            env_build.make(args=["install"])

    def package(self):
        self.copy("LICENSE", src=self.libpcap_dir, dst="licenses")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            if self.options.enable_dbus:
                self.cpp_info.libs.append("dbus-glib-1")
                self.cpp_info.libs.append("dbus-1")
            if self.options.enable_bluetooth:
                self.cpp_info.libs.append("bluetooth")
            if self.options.enable_packet_ring:
                self.cpp_info.libs.append("nl-genl-3")
                self.cpp_info.libs.append("nl-3")
