import sys
from cx_Freeze import setup, Executable

base = "Win32GUI"
path_platforms = [("D:/apps\Python34_32\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll",
"platforms\qwindows.dll"),('D:\\apps\Python34_32\Lib\site-packages\PyQt5\libEGL.dll', 'libEGL.dll')]
build_options = {"includes" : [ "re", "atexit" ], "include_files" :  path_platforms}

setup(
    name = "simple_PyQt5",
    version = "0.1",
    description = "Sample cx_Freeze PyQt4 script",
    options = {"build_exe" : build_options},
    executables = [Executable("mainframe.py", base = base)]
    )