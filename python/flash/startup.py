import os,zipfile

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
    (options,var) = startup.parseCmdLine()
    extraction = options.ensure_value('extraction',None)

    parameters = startup.buildsystemcommandline(var)
    #unzip theSCVPackage.7z
    print 'parameters %s'% parameters
    if extraction and os.path.exists(extraction):

        os.system('7z x %s -y'%extraction)

    if os.path.exists('execute.py'):
        os.system('python execute.py %s'%parameters)
    else:
        print 'execute.py not found'
