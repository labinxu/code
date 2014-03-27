#setting the path environment
import os, platform,shutil,sys
import getopt

#################################
path_separate = ':'
dir_separate='/'
if platform.system() == 'Windows':
    path_separate=';'
    dir_separate='\\'

optShortVars=''
optLongVars=''
#########################################
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

############################################
def copytree(src, dst, symlinks=False):  
    names = os.listdir(src)  
    if not os.path.isdir(dst):  
        os.makedirs(dst)  
          
    errors = []  
    for name in names:  
        srcname = os.path.join(src, name)  
        dstname = os.path.join(dst, name)  
        try:  
            if symlinks and os.path.islink(srcname):  
                linkto = os.readlink(srcname)  
                os.symlink(linkto, dstname)  
            elif os.path.isdir(srcname):  
                copytree(srcname, dstname, symlinks)  
            else:  
                if os.path.isdir(dstname):  
                    os.rmdir(dstname)  
                elif os.path.isfile(dstname):  
                    os.remove(dstname)  
                shutil.copy2(srcname, dstname)  
            # XXX What about devices, sockets etc.?  
        except (IOError, os.error) as why:  
            errors.append((srcname, dstname, str(why)))  
        # catch the Error from the recursive copytree so that we can  
        # continue with other files  
        except OSError as err:  
            errors.extend(err.args[0])  
    try:  
        shutil.copystat(src, dst)  
    except WindowsError:  
        # can't copy file access times on Windows  
        pass  
    except OSError as why:  
        errors.extend((src, dst, str(why)))  
    if errors:  
        raise Error(errors) 

def help():
    help_str='''usage: [--app] [--help] [--source_dir]\n
    -a,-app              The application name don't contain the extent name
    -s,--source_dir      The source directory,
    -p --append pach a subdirectory
    '''
    return help_str

def getdir(_title):
    import tkFileDialog
    d = tkFileDialog.askdirectory(title = _title)
    pos = d.rfind('/')
    if pos != -1:
        return (d,d[pos+1:])
    return (d,None)

def getAppdir(dirs,appname):

    for dir in dirs:
        for root,dirs,files in os.walk(dir,topdown=True):
            for file in files:
               # print file
                if file == appname+'.exe' or file == appname or file == appname+'.sh' :
                    return dir
    return None

def get_app_sys_path(appname):
    #
    filename=os.environ.get('path')
    paths = [name for name in filename.split(path_separate) if name.lower().find(appname.lower())!=-1]
    return getAppdir(paths,appname)

def copy_dir(src,dest):
    '''
    replace the files if it exist
    '''
    for item in os.listdir(src):
        if os.path.isdir(os.path.join(src, item)):
            copytree(os.path.join(src,item), os.path.abspath(os.path.join(dest, item)))
            print 'copy %s to %s'%(os.path.join(src, item), os.path.abspath(os.path.join(dest, item)))
        elif os.path.isfile(os.path.join(src, item)):
         #   print '%s is file'%item
            shutil.copy(os.path.join(src,item), dest)
            print 'copy %s to %s'%(os.path.join(src,item), os.path.abspath(dest))
def parseCmdLine():
    '''
    opts:
    --application application name
    --dest_dir copy dest directory
    --souce_dir application dir if no --app opt
    --append pach a subdirectory
    short apts
    -a,-s,-d ,-p
    
    '''
    optlist,var = getopt.getopt(sys.argv[1:],'?h:a:p:s:d:r',['run=','application=','help','source_dir=','dest_dir='])
    #call python copytools.py -a ruby -p ".." -s %~dp0BDD/ruby
    #optlist=[('-a','ruby'),('-p','..'),('-s','./BDD/ruby')]
    for opt,var in optlist:
        if opt in ['-h','--help','-?']:
            print help()
            return None
    return optlist

#print 'python path', get_app_sys_path('python')
def get_src_dest_dirs(optlist):
    
    src_dir=[]
    dest_dir=[]
    append_dir=None
    for opt,var in optlist:
        # from the application name get dest dir
        if opt in ['-a','--application']:
            for item in var.split(','):
                ds=checkAppPath(item)
                if not ds:
                    print 'can not find %s'%item
                    continue
                dest_dir.append(ds)
        elif opt in ['-s','--source_dir']:
            src_dir=var.split(',')
        elif opt in ['-p','--append']:
            append_dir=var
        else:
            dest_dir=var.split(',')
    assert len(src_dir) == len(dest_dir)
    #append the dirs
    for i in range(len(dest_dir)):
        if dest_dir[i][-1] != dir_separate:
            dest_dir[i] += dir_separate
    if append_dir:
        dest_dir = map(lambda x : x + append_dir,dest_dir)
    return zip(src_dir,dest_dir)

def get_directoryname(path):
    path =path.replace('\\','/')
    pos = path.rfind('/')
    if pos != -1:
        return path[pos+1:]
    return None

def checkEnv(name):
    '''
    check wheather the name is in environment settings
    '''
    assert len(name)>0

    env = CreateEnvhelper(scope='system')
    ret = env.getenv(name)
    if ret:
        print "%s is %s"%(name,ret)
        return True
    else:
        env = CreateEnvhelper(scope='user')
        ret = env.getenv(name)
        if ret:
            print "%s is %s"%(name,ret)
            return True
        
    print '%s is not exist'%name
    return False

def setEnv(name,value):
    env = CreateEnvhelper()
    env.setenv(name,value)
    print 'set %s %s'%(name,value)

def checkAppPath(appname,dirName=None,path='path'):
    #
    msg = 'check %s in path'%appname
    env = CreateEnvhelper(scope='system')
    filename = env.getenv(path)
    if not dirName:
        paths = [name for name in filename.split(path_separate) if name.lower().find(appname.lower())!=-1]
    else:
        paths = [name for name in filename.split(path_separate) if name.lower().find(dirName.lower())!=-1]
    dir = getAppdir(paths,appname)
    if dir:
        print '%s OK %s'%(msg,dir)
        return dir
    else:
        env = CreateEnvhelper(scope='user')
        filename = env.getenv(path)
        if not dirName:
            paths = [name for name in filename.split(path_separate) if name.lower().find(appname.lower())!=-1]
        else:
            paths = [name for name in filename.split(path_separate) if name.lower().find(dirName.lower())!=-1]
        dir = getAppdir(paths,appname)
        if dir:
            print '%s OK %s'%(msg,dir)
            return dir

    print '%s NOK \npath:%s'%(msg,filename)
    return None
def getParams(param,optlist):
    for opt,var in optlist:
        pass
def main():
    ###init step 1.check android home
    if not checkEnv('ANDROID_HOME'):
        return
    ###step 2. check android sdk
    if not checkAppPath('adb','platform-tools'):
        return
    ###step 3. check ruby in path
    if not checkAppPath('ruby'):
        return
    ###invoke setup bat
    absCurrentDir = os.path.abspath('.')
    setupDir =os.path.join(absCurrentDir ,'Appium/pythonWebdriver/setup.bat')
    print setupDir
    os.system(setupDir)
    ###
    
    optlist = parseCmdLine()
    if optlist:
        src_dest_dirs = get_src_dest_dirs(optlist)
        for src,dest in src_dest_dirs:
            copy_dir(src,dest)

    ###check debug.keystore
    homeDir = os.path.expanduser('~')
    androidDir = os.path.join(homeDir,'.android')
    if not os.path.exists(androidDir):
        os.system('mkdir %s'%androidDir)

    keystoreDir = os.path.join(androidDir,'debug.keystore')
    if not os.path.exists(keystoreDir):
        print 'copy %s to %s'%(os.path.join(absCurrentDir,'debug.keystore'),keystoreDir)
        shutil.copy(os.path.join(absCurrentDir,'debug.keystore'),keystoreDir)
        
    #if not exist %USERPROFILE%\.android mkdir %USERPROFILE%\.android
    #if not exist %USERPROFILE%\.android\debug.keystorre copy %~dp0debug.keystore %USERPROFILE%\.android
    
if __name__=='__main__':
    main()
