import sys

from cx_Freeze import setup, Executable

build_exe_options = {
    "packages" : ['src']
}
setup (
    name = 'server',
    version = "0.0.1",
    discription = "server",
    options = {
        "build_exe" : build_exe_options
    },
    executables = [Executable('src/server_class.py')]
)