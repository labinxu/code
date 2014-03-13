#--*-- coding utf-8 --*--
#setting the path environment
import os, platform,shutil,sys
import getopt


path_separate = '.:'
dir_separate='/'
if platform.system() == 'Windows':
    path_separate=';'
    dir_separate='\\'

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
                if file == appname+'.exe':
                    return dir
    return None

def copy_dir(src,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src,dest)
def parseCmdLine():
    '''
    opts:
    --app application name
    --dest_dir copy dest directory
    --souce_dir application dir if no --app opt
    short apts
    -a,-s,-d
    
    '''
    optlist,var = getopt.getopt(sys.argv[1:],'?h:a:s:d:',['app=','source_dir=','dest_dir='])
    # if there are more than three opts input ,take two of them
    if len(optlist) > 2:
        optlist = optlist[0:2]
        print 'more than two opts input take front two'

    return optlist

#print 'python path', get_app_sys_path('python')
def get_src_dest_dirs(optlist):
    if len(optlist) > 2:
        optlist = optlist[0:2]
        print 'more than two opts input take front two'
    assert len(optlist)==2

    src_dir=[]
    dest_dir=[]
    for opt,var in optlist:
        print opt,var
        # from the application name get dest dir
        if opt in ['-a','--app']:
            for item in var.split(','):
                ds=get_app_sys_path(item)
                if not ds:
                    print 'can not find %s'%item
                    continue
                dest_dir.append(ds)
        elif opt in ['-s','--source_dir']:
            src_dir=var.split(',')
        else:
            dest_dir=var.split(',')
    assert len(src_dir) == len(dest_dir)
    return zip(src_dir,dest_dir)
def get_directoryname(path):
    path =path.replace('\\','/')
    print 'get name',path
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
    src_dest_dirs = get_src_dest_dirs(optlist)
    print src_dest_dirs
    
    for src,dest in src_dest_dirs:
        print 'copy %s to %s'%(src,dest)
        
        copy_dir(src,dest+dir_separate+get_directoryname(src))
   
