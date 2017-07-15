"""This script build Conan.io package to multiple platforms."""
from os import getenv
from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.password = getenv("CONAN_PASSWORD")
    builder.add_common_builds(shared_option_name="libpcap:shared", pure_c=True)
    for settings, options, env_vars, build_requires in reversed(builder.builds):
        false_options = dict(options)
        false_options["enable_usb"] = False
        false_options["enable_bluetooth"] = False
        false_options["enable_dbus"] = False
        false_options["enable_packet_ring"] = False
        builder.builds.append([settings, false_options, env_vars, build_requires])
    builder.run()
