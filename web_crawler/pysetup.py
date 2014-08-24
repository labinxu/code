# mysetup.py
from distutils.core import setup
import py2exe


py2exe_options = {
'includes':['sip','ctypes','PyQt5',
'PyQt5.QtCore', 'PyQt5.QtGui','manager', 'typesdefine',
'windows_tp', 'utils','sites' ,'db','concurrent','concurrent.futures', 'urllib.request',
'bs4','typesdefine.data_types'],
'compressed':0,
'optimize':2,
'ascii':0,
'bundle_files':1}

setup(
name = 'Crawler',
version = '1.0',
windows = ['testpy2exe.py'],
options = {'py2exe':py2exe_options}
)