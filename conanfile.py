from conans import ConanFile, MSBuild, tools
from shutil import copyfile
import os

class ImGuiConan(ConanFile):
    name = "imgui"
    license = "https://github.com/ocornut/imgui/blob/master/LICENSE.txt"
    description = "Dear ImGui: Bloat-free Immediate Mode Graphical User interface for C++ with minimal dependencies"
    url = "https://github.com/ocornut/imgui"

    # Setting and options
    settings = "os", "compiler", "arch"

    # Additional files to export
    exports_sources = ["premake5.lua"]

    # Iceshard conan tools
    python_requires = "conan-iceshard-tools/0.5.2@iceshard/stable"
    python_requires_extend = "conan-iceshard-tools.IceTools"

    def init(self):
        self.ice_init("premake5")
        self.build_requires = self._ice.build_requires

    # Override the source entry method
    def ice_source_entry(self, version):
        # We are appending '-docking' string so the right entry from 'conandata.yml' file is picked.
        if self.channel == "docking":
            return "{}-docking".format(version)
        else:
            return version

    # Build both the debug and release builds
    def ice_build(self):
        copyfile("../premake5.lua", "premake5.lua")
        self.ice_generate()

        if self.settings.compiler == "Visual Studio":
            self.ice_build_msbuild("imgui.sln", ["Debug", "Release"])

        else:
            self.ice_build_make(["Debug", "Release"])

    def package(self):
        self.copy("LICENSE.txt", src=self._ice.out_dir, dst="LICENSE")

        self.copy("*.h", "include/imgui", src=self._ice.out_dir, keep_path=True, excludes=("examples/*", "misc/*"))

        build_dir = os.path.join(self._ice.out_dir, "bin")
        if self.settings.os == "Windows":
            self.copy("*.lib", "lib", build_dir, keep_path=True)
        if self.settings.os == "Linux":
            self.copy("*.a", "lib", build_dir, keep_path=True)

    def package_info(self):
        self.cpp_info.debug.libdirs = [ "lib/Debug" ]
        self.cpp_info.release.libdirs = [ "lib/Release" ]
        self.cpp_info.libdirs = []
        self.cpp_info.libs = ["imgui"]
