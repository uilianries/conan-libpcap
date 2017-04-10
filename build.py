"""This script build Conan.io package to multiple platforms."""
from platform import system
from os import getenv
from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.password = getenv("CONAN_PASSWORD")
    builder.add_common_builds(shared_option_name="libpcap:shared", pure_c=True)
    if system() == "Linux":
        stdlibcpp11_builds = []
        for settings, options in builder.builds:
            settings["compiler.libcxx"] = "libstdc++"
            if settings["compiler.version"] > "4.9":
                _settings = dict(settings)
                _settings["compiler.libcxx"] = "libstdc++11"
                stdlibcpp11_builds.append([_settings, options])
        builder.builds = builder.builds + stdlibcpp11_builds
    builder.run()
