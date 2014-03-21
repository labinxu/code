#coding utf-8

import sys,platform
if sys.hexversion > 0x03000000:
    import winreg
else:
    import _winreg as winreg
from subprocess import check_call    

class Environment(object):
    def getPlatform(self):
        return platform.system()
    
    def __init__(self,scope):
        pass
    def __getattr__(self,name):
        print 'getattr%s'%name
        return getattr(self,name)
    def getenv(self,name):
        pass
class WinEnvironment(Environment):
    def __init__(self,scope):
        Environment.__init__(self,scope)
        assert scope in ('user','system')
        if scope == 'user':
            self.root = winreg.HKEY_CURRENT_USER
            self.subkey = 'Environment'
        else:
            self.root = winreg.HKEY_LOCAL_MACHINE
            self.subkey = r'SYSTEM\CurrentcontrolSet\Control\Session Manager\Environment'
    def getenv(self,name):
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_READ)
        try:
            value,_ = winreg.QueryValueEx(key,name)
        except WindowsError:
            value = ''
        return value
    def setenv(self,name,value):
        value.replace('/','\\')
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
        winreg.CloseKey(key)

    def append(self,name,value):
        vars = self.getenv(name)
        if vars.find(value) == -1:
            value = '%s;%s'%(vars,value)
            self.setenv(name,value)
        else:
            print '%s is exist'%value

def CreateEnvhelper(scope = 'user'):
    
    if platform.system() == 'Windows':
        environ = WinEnvironment(scope)
    else:
        environ =None
    return environ

















