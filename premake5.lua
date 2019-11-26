newoption {
    trigger = "arch",
    description = "Build for the given architecture",
    value = "ARCH"
}

workspace "imgui"
    configurations { "Debug", "Release" }
    debugformat "C7"

    architecture(_OPTIONS.arch)

    filter { "Debug" }
        symbols "On"

    filter { "Release" }
        optimize "On"

    project "imgui"
        kind("StaticLib")

        includedirs {
            "."
        }

        files {
            "*.h",
            "*.cpp",
        }

        filter "toolset:msvc"
            files { "misc/natvis/*.natvis" }
