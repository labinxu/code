import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit',
        'include_files':"D:/apps\Python34\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll"
    }
}

executables = [
    Executable('mainframe.py', base=base)
]

setup(name='QiTong',
      version='0.1',
      description='main frame',
      options=options,
      executables=executables
      )