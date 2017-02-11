from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(upload=True)
    builder.add_common_builds()
    builder.run()
