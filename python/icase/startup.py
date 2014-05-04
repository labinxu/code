
import os

class StartupHelper():
    def parseCmdLine(self):
                
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-x',"--extraction", help = 'extration file')
        return parser.parse_args()
    def buildsystemcommandline(self, command):
        counter = 1
        args=''
        parameter=''
        print 'parse command %s'%command
        for item in command:
            if counter % 2 != 0:
                args = '--%s ' % item
            else:
                args = '%s%s '%(args,item)
                parameter += args
            counter +=1
        if counter ==2:
            return args        
        return parameter

if __name__=='__main__':

    startup = StartupHelper()
    (options,parameters) = startup.parseCmdLine()
    extraction = options.ensure_value('extraction',None)
    #parameters = "--parameters --thrill -v -v -v -s 200 10000"
    #python startup.py "\"--testtype\" \"monkey\" \"--product\" \"devices.json\" \"--parameters\" \"--thrill -v -v -v -s 200 10000\""
    #python startup.py "\"--testtype\" \"marble\" \"--product\" \"devices.json\" \"--testset\" \"..\test_sets\marble_self_tests.testset\" \"--marbletool\" \".\marble\""
    #python startup.py "\"--testtype\" \"robotium\" \"--product\" \"devices.json\" \"--apk\" \"notepad.apk\" \"--package\" \"com.anoid.notepad\" \"--testapk\" \"rt_NotePad.apk\" \"--testpackage\" \"com.notepadblackboxtest\" \"--runner\" \"android.test.InstrumentationTestRunner\""

    #unzip theSCVPackage.7z
    import glob
    #    zips = glob.glob(os.path.join(os.path.abspath(os.getcwd()),'*.zip'))
    zips = glob.glob("*.zip")
    print zips
    for zip in zips:
        print '7z x %s -y'%zip
        os.system('7z x %s -y'%zip)
    if os.path.exists('execute.py'):
        print 'python execute.py %s'%parameters[0]
        os.system('python execute.py %s'% parameters[0])
    else:
        print 'execute.py not found'
