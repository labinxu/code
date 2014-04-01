#coding utf-8

import sys,platform
if sys.hexversion > 0x03000000:
    import winreg
else:
    import _winreg as winreg

class Environment(object):
    
    def getPlatform(self):
        return platform.system()
    
    def __init__(self):
        
        self.pathSeparate = None

    def __getattr__(self,name):
        print 'getattr%s'%name
        return getattr(self,name)

    def getenv(self,name):
        pass

class WinEnvironment(Environment):
    def __init__(self):
        Environment.__init__(self)
        self.envPathSeparate = ";"

    def getUserEnv(self, name):

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment', 0, winreg.KEY_READ)
        try:
            value,_ = winreg.QueryValueEx(key,name)
        except WindowsError:
            value = ''

        return value

    def getSystemEnv(self, name):

        subkey = r'SYSTEM\CurrentcontrolSet\Control\Session Manager\Environment'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,subkey, 0, winreg.KEY_READ)
        try:
            value,_ = winreg.QueryValueEx(key,name)
        except WindowsError:
            value = ''

        return value
        
    def getenv(self,name):
        
        userEnv = self.getUserEnv(name)
        systemEnv = self.getSystemEnv(name)

        ret = ''
        if userEnv:
            ret += userEnv
            
        if ret:
            if systemEnv:
                return ret + self.envPathSeparate + systemEnv
            
            return ret

        return None

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

class LinuxEnvironment(Environment):
    def __init__(self):
        self.envPathSeparate = ":"
        
    def getenv(self, name):
        pass
    def setenv(self, name, value):
        pass
        
def CreateEnvhelper():
    
    if platform.system() == 'Windows':
        environ = WinEnvironment()
    else:
        environ = LinuxEnvironment()
    return environ

















