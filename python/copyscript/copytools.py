#setting the path environment
import os, platform,shutil,sys
import getopt


path_separate = ':'
dir_separate='/'
if platform.system() == 'Windows':
    path_separate=';'
    dir_separate='\\'

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

def get_app_sys_path(appname):
    #
    filename=os.environ.get('path')
    paths = [name for name in filename.split(path_separate) if name.find(appname)!=-1]
    for dir in paths:
        for root,dirs,files in os.walk(dir,topdown=True):
            for file in files:
               # print file
                if file == appname+'.exe' or file == appname or file == appname+'.sh' :
                    return dir
    return None

def copy_dir(src,dest):
   #if os.path.exists(dest):
   #    shutil.rmtree(dest)
    copytree(src,dest)
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
    optlist,var = getopt.getopt(sys.argv[1:],'?h:a:p:s:d:',['application=','help','source_dir=','dest_dir='])
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
        print opt,var
        # from the application name get dest dir
        if opt in ['-a','--application']:
            for item in var.split(','):
                ds=get_app_sys_path(item)
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

def main():
    content=raw_input('Enter the app name separate by \';\' :')
    for item in content.split(';'):
        if len(item) >0:
            destdir=get_app_sys_path(item)
            if destdir==None:
                print 'can not path %s' % item
                continue
            print 'dest dir is:',destdir
            src_dir,dir_name=getdir('Select source folder')
            if src_dir==None or dir_name == None:
                print 'these is no select '
                continue
            print 'src folder is:' ,src_dir,dir_name
            copy_dir(src_dir,destdir+dir_separate+dir_name)

if __name__=='__main__':
    optlist = parseCmdLine()
    if optlist:

        src_dest_dirs = get_src_dest_dirs(optlist)
        for src,dest in src_dest_dirs:
            print 'copy %s to %s'%(src,dest)

            copy_dir(src,dest+dir_separate+get_directoryname(src))

