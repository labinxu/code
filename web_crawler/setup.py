import sys
from cx_Freeze import setup, Executable

  
includes = ['atexit', 'sys','PyQt5.QtCore','PyQt5.QtGui', 'PyQt5.QtWidgets']
excludes = []
include_files=[('d:\\apps\Python34_32\Lib\site-packages\PyQt5\libEGL.dll', 'libEGL.dll')]
packages = ['sites']
path = []
base = None
name = 'mainframe.exe'


if sys.platform == 'win32':
    base = 'Win32GUI'
options = {
    'build_exe': {
        "includes": includes,
        "excludes": excludes,
        "packages": packages,
        'include_files':include_files,
        "path": path
    }
}
executables = [Executable('gui/mainframe.py', base=base)]
setup(name=name,
      version='0.1',
      description='Sample PyQT5-matplotlib script',
      executables=executables,
      options=options
      )