"""Conan.io recipe for pcap library
"""
import os
from tempfile import mkdtemp
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
    url = "http://github.com/uilianries/conan-libpcap"
    author = "Uilian Ries <uilianries@gmail.com>"
    description = "An API for capturing network traffic"
    license = "https://github.com/the-tcpdump-group/libpcap/blob/master/LICENSE"
    default_options = "shared=True", "enable_dbus=False", "enable_bluetooth=False", "enable_usb=False", "enable_packet_ring=False", "disable_universal=False"
    libpcap_dir = "%s-%s-%s" % (name, name, version)
    install_dir = mkdtemp(suffix=name)

    def requirements(self):
        if self.options.enable_usb:
            self.requires("libusb/1.0.21@uilianries/stable")

    def build_requirements(self):
        if self.settings.os == "Linux":
            self.build_requires("bison/3.0.4@uilianries/stable")
            self.build_requires("flex/2.6.4@uilianries/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

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
        if self.settings.os != "Windows":
            tools.get("https://github.com/the-tcpdump-group/libpcap/archive/libpcap-%s.tar.gz" % self.version)
        else:
            # Get Winpcap 4.1.3
            url = "https://github.com/patmarion/winpcap"
            self.run("git clone %s %s" % (url, self.libpcap_dir))

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        if self.settings.os != "Windows":
            with tools.chdir(self.libpcap_dir):
                env_build = AutoToolsBuildEnvironment(self)
                configure_args = ["--prefix=%s" % self.install_dir]
                configure_args.append("--enable-shared" if self.options.shared else "--disable-shared")
                configure_args.append("--disable-universal" if not self.options.disable_universal else "")
                configure_args.append("--enable-dbus" if self.options.enable_dbus else "--disable-dbus")
                configure_args.append("--enable-bluetooth" if self.options.enable_bluetooth else "--disable-bluetooth")
                configure_args.append("--enable-usb" if self.options.enable_usb else "--disable-usb")
                configure_args.append("--enable-packet-ring" if self.options.enable_packet_ring else "--disable-packet-ring")
                # Cross compile x86_64 to x86 needs --with-pcap
                if self.settings.os == "Macos" and self.settings.arch == "x86":
                    configure_args.append("--with-pcap=null")
                env_build.fpic = True
                env_build.configure(args=configure_args)
                env_build.make(args=["all"])
                env_build.make(args=["install"])

    def package(self):
        self.copy("LICENSE", src=self.libpcap_dir, dst=".")
        if self.settings.os != "Windows":
            self.copy(pattern="*.h", dst="include", src=os.path.join(self.install_dir, "include"))
            if self.options.shared:
                self.copy(pattern="*.so*", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
                self.copy(pattern="*.dylib", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
        else:
            wpcap_dir = os.path.join(self.build_folder, self.libpcap_dir)
            self.copy(pattern="*.h", dst="include", src=os.path.join(wpcap_dir, "Include"))
            if self.settings.arch == "x86_64":
                self.copy(pattern="*.dll", dst="bin", src=os.path.join(wpcap_dir, "Lib", "x64"), keep_path=False)
                self.copy(pattern="*.lib", dst="lib", src=os.path.join(wpcap_dir, "Lib", "x64"), keep_path=False)
            else:
                self.copy(pattern="wpcap.dll", dst="bin", src=os.path.join(wpcap_dir, "Lib"), keep_path=False)
                self.copy(pattern="Packet.dll", dst="bin", src=os.path.join(wpcap_dir, "Lib"), keep_path=False)
                self.copy(pattern="wpcap.lib", dst="lib", src=os.path.join(wpcap_dir, "Lib"), keep_path=False)
                self.copy(pattern="Packet.lib", dst="lib", src=os.path.join(wpcap_dir, "Lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
        if self.settings.os == "Linux":
            if self.options.enable_dbus:
                self.cpp_info.libs.append("dbus-glib-1")
                self.cpp_info.libs.append("dbus-1")
            if self.options.enable_bluetooth:
                self.cpp_info.libs.append("bluetooth")
            if self.options.enable_packet_ring:
                self.cpp_info.libs.append("nl-genl-3")
                self.cpp_info.libs.append("nl-3")
