import os
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
def copy_dir(src,dest):
    '''
    replace the files if it exist
    '''
    for item in os.listdir(src):
        if os.path.isdir(os.path.join(src, item)):
            copytree(os.path.join(src,item), os.path.abspath(os.path.join(dest, item)))
            print 'copy %s to %s'%(os.path.abspath(os.path.join(src, item)),\
                                    os.path.abspath(os.path.join(dest, item)))
        elif os.path.isfile(os.path.join(src, item)):
            shutil.copy(os.path.join(src,item), dest)
            print 'copy %s to %s'%(os.path.abspath(os.path.join(src,item)), os.path.abspath(dest))

if __name__=='__main__':

    #unzip theSCVPackage.7z
    import glob ,importlib
    zips = glob.glob("*.zip")
    for zip in zips:
        print '7z e %s -y'%zip
        os.system('7z x %s -y'%zip)
    if os.path.exists('./icase'):
        copy_dir('./icase','.')
    if os.path.exists('execute.py'):
        execute = importlib.import_module('execute')
        execute.main()
    else:
        print 'execute.py not found'
