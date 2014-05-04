import os
if __name__=='__main__':

    #unzip theSCVPackage.7z
    import glob ,importlib
    zips = glob.glob("*.zip")
    for zip in zips:
        print '7z x %s -y'%zip
        os.system('7z x %s -y'%zip)
    if os.path.exists('execute.py'):
        execute = importlib.import_module('execute')
        execute.main()
    else:
        print 'execute.py not found'
