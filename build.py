"""This script build Conan.io package to multiple platforms."""
import platform
from copy import copy
from conan.packager import ConanMultiPackager
from conan.builds_generator import BuildConf


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="libpcap:shared", pure_c=True)
    builder.run()
