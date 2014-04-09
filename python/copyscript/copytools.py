#setting the path environment
import shutil,os,sys
import getopt

import installTools

#install tools instance
insTools = installTools.SetUptools()
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
        raise OSError(errors) 

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

def copy_dir(src,dest):
    '''
    replace the files if it exist
    '''
    for item in os.listdir(src):
        if os.path.isdir(os.path.join(src, item)):
            copytree(os.path.join(src,item), os.path.abspath(os.path.join(dest, item)))
            print 'copy %s to %s'%(os.path.join(src, item),\
                                    os.path.abspath(os.path.join(dest, item)))
        elif os.path.isfile(os.path.join(src, item)):
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
    optlist,var = getopt.getopt(sys.argv[1:],'?h:a:p:s:d:e',
                                ['execute=','application=','help','source_dir=','dest_dir='])
    #call python copytools.py -a ruby -p ".." -s %~dp0BDD/ruby
    #optlist=[('-a','ruby'),('-p','..'),('-s','./BDD/ruby')]
    for opt,var in optlist:
        if opt in ['-h','--help','-?']:
            print help()
            return None
    return optlist

#print 'python path', get_app_sys_path('python')
def get_src_dest_dirs(optlist):
    '''
    get a application's dir and append the command suffix path
    '''
    src_dir=[]
    dest_dir=[]
    append_dir=None
    for opt,var in optlist:
        # from the application name get dest dir
        if opt in ['-a','--application']:
            for item in var.split(','):
                ds=insTools.checkAppPath(item)
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
    if append_dir:
        dest_dir = map(lambda x : os.path.join(x, append_dir), dest_dir)

    return zip(src_dir,dest_dir)

def getParams(optlist):
    cmdVar = {}
    for opt,var in optlist:
        if opt in ['-a','--application']:
            cmdVar['a'] = var
        elif opt in ['-s','--source_dir']:
            cmdVar['s'] = var
        elif opt in ['-p','--append']:
            cmdVar['p'] = var
        elif opt in ['-e','--execute']:
            cmdVar['e'] = var
    return cmdVar

def main():

    cmdVar={}
    optlist = parseCmdLine()
    if optlist:
        cmdVar = getParams(optlist)

    ###init step 1.check android home

    if not insTools.checkEnv('ANDROID_HOME'):
        return
    
    ###step 2. check android sdk
    if not insTools.checkAppPath('adb','platform-tools'):
        return
    
    ###step 3. check ruby in path
    if not insTools.checkAppPath('ruby'):
        return

    ###invoke setup bat
    execPath = None
    if cmdVar:
        if cmdVar.has_key('e'):
            execPath = cmdVar['e']
    if not execPath:
        execPath = './Appium/pythonWebdriver/setup.bat'
    
    absCurrentDir = os.path.abspath('.')
    
    setupDir =os.path.join(absCurrentDir ,execPath)
    os.system(setupDir)
    ###
    
    if not optlist:
        optlist = [('-a', 'ruby'), ('-p', '..'), ('-s', './BDD/ruby')]

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
        
if __name__=='__main__':
    main()


