import os,zipfile,subprocess,time,sys,threading,shutil
import junit_parser

class CommandWatchCat(threading.Thread):
    def __init__(self, popen,timeout):
        threading.Thread.__init__(self)
        self.popen = popen
        self.timeout = timeout
    def run(self):
        time.sleep(self.timeout)
        print 'terminate command'
#        self.popen.
        self.popen.terminate()
        time.sleep(10)

class UtilsHelper():
    def __init__(self):
        import platform
        if platform.system() == 'Windows':
            self.isWindows = True
        else:
            self.isWindows = False
        self.workspace = os.path.abspath(os.getcwd())
    def copytree(self,src, dst, symlinks=False):  
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
                    self.copytree(srcname, dstname, symlinks)  
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

    def copyFolderContents(self,src,dest):
        '''
        replace the files if it exist
        '''
        for item in os.listdir(src):
            if os.path.isdir(os.path.join(src, item)):
                self.copytree(os.path.join(src,item), os.path.abspath(os.path.join(dest, item)))
                print 'copy %s to %s'%(os.path.abspath(os.path.join(src, item)),\
                                       os.path.abspath(os.path.join(dest, item)))
            elif os.path.isfile(os.path.join(src, item)):
                shutil.copy(os.path.join(src,item), dest)
                print 'copy %s to %s'%(os.path.abspath(os.path.join(src,item)), os.path.abspath(dest))
            
    def runCommand(self,logger,command,timeout = None):
        exitcode = 0
        print 'run %s'%command
        try:
            counter = 3
            while(counter > 0): 
                tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                #create a command watch cat
                if timeout:
                    CommandWatchCat(tool,timeout = timeout).start()
                toolOutputs = tool.stdout
                while 1: 
                    outputFromTool = toolOutputs.readline() 
                    time.sleep(1/10) 
                    if not outputFromTool: 
                        break 
                    print 'Tool: ' + outputFromTool 
                    logger.append(outputFromTool)
                exitcode = tool.wait()
                print 'process return %d,counter %d'%(exitcode,counter)
                if exitcode !=0:
                    print 'execute faild %s'%command
                    sys.stdout = sys.__stdout__
                    counter -= 1
                    break
                else:
                    sys.stdout = sys.__stdout__
                    #wait  the process totally terminate
                    print 'Tool execution finished' 
                    break
        except OSError, e:
            sys.stdout = sys.__stdout__
            print 'An error occured during execution: ', e 
            return exitcode

    def setWorkspace(self,new_workspace):
        self.workspace = new_workspace

    def installTesthelper(self,product):
        print 'Enter install test helper'
        directory = os.path.join(self.workspace,'utils','TestHelpers.jar')
        if os.path.exists(os.path.join(self.workspace,'utils','TestHelpers.jar')):
            if not os.path.exists('results'):
                os.makedirs('results')

            logger = Logger('results','flash.log')

            cmd ='adb -s %s push %s /data/local/tmp'%(product.sn, directory)
            self.runCommand(logger,cmd)
            cmd ='adb -s %s shell pm disable com.nokia.FirstTimeUse/com.nokia.FirstTimeUse.LanguageSelection'%product.sn
            self.runCommand(logger,cmd)

            cmd ='adb -s %s shell pm disable com.nokia.FirstTimeUse/com.nokia.FirstTimeUse.Warranty'%product.sn
            self.runCommand(logger,cmd)
            cmd = 'adb -s %s root'%product.sn
            self.runCommand(logger,cmd)
            cmd = 'adb -s %s shell rm -rf /storage/sdcard1/*'%product.sn
            self.runCommand(logger,cmd)

#            cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c com.testhelpers.DeviceInitialization -e timeout 500'%product.sn
            #self.runCommand(logger,cmd,timeout=500)
            
    def unlockPhone(self,logger,product):
        securityCode = self.getSecurityCode(product.productName)
        cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c com.testhelpers.DeviceUnlock -e securitycodes %s'%(product.sn,securityCode)
        self.runCommand(logger,cmd)
    def addDirArchive(self,archiveName,startdir):

        print 'add %s to %s'%(startdir,archiveName)
        with zipfile.ZipFile(archiveName,'w',zipfile.ZIP_DEFLATED) as f:
            for dirpath, dirnames, filenames in os.walk(startdir):
                for filename in filenames:
                    print 'add %s'%(os.path.join(dirpath,filename))
                    f.write(os.path.join(dirpath,filename))

    def addArchive(self, archiveName,filename):
        print 'add %s to %s' % (archiveName, filename)
        with zipfile.ZipFile(archiveName, 'a') as myzip:
            myzip.write(filename)
    def getSecurityCode(self, productName):
        print 'open %s'% os.path.join(self.workspace,'utils/seccode.txt')
        with open(os.path.join(self.workspace,'utils/seccode.txt')) as f:
            for line in f.readlines():
                if productName in line:
                    return line.split('=')[1]
        return None

    def addArchives(self, archiveName,files):
        with zipfile.ZipFile(archiveName, 'a') as myzip:
            for file in files:
                print 'add %s to %s'%(archiveName,file)
                myzip.write(file)

    def findfiles(self,targetdirectory):
        results = []
        for root,dirs,files in os.walk(targetdirectory):
            for fn in files:
                results.append(os.path.join(root,fn))
        return results

    def parseCmdLine(self):
                
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-p', '--product', dest = 'product', help = 'contains product information')
        parser.add_option('-f', '--flash', dest = 'flash',help = 'flash tool name and path')
        
        parser.add_option('-T','--testtype',dest = 'testtype',help = 'type of the test eg: marble ,instrument,Monkey...')
        
        #marble params
        parser.add_option('-A', '--marbletool',dest = 'marbletool',help ='marble tools name eg: ../marble.py')
        parser.add_option('-t', '--testset', dest ='testset', help='test case configure contains test case')
        
        #instrument params
        parser.add_option('-a', '--apk',dest = 'apk',help ='apk name')
        parser.add_option('-k', '--package',dest = 'package',help ='package name')
        parser.add_option('-e', '--testapk',dest = 'testapk',help ='testapk name')
        parser.add_option('-c', '--testpackage',dest = 'testpackage',help ='testpackage name')
        parser.add_option('-r', '--runner',dest = 'runner',help ='runner name')
        
        #Monkey command
        parser.add_option('-O', '--Monkey', dest = 'Monkey', help = 'Monkey test')
        
        parser.add_option('-P', '--parameters',dest = 'parameters',help ='marble tools name eg: ../marble.py')
        return parser.parse_args()
    
utilsHelper = UtilsHelper()

class Parse(object):
    
    def parse(self):
        return None
    def getJsonName(self, jsonfilename):
        return jsonfilename[0:-5]

class JunitParser(object):
    def __init__(self):
        pass
        
    def parse(self,destfile):
        junit_parser.parse(destfile)
        
class Logger:
    def __init__(self,dir,logfile):
        self.filename = logfile
        self.logpath = os.path.abspath(os.path.join(dir,logfile))
        self.logfile = open(os.path.abspath(os.path.join(dir,logfile)),'w')
        self.workspace = dir
        self.zipResult = None
    def append(self,log):
        self.logfile.write(log)
        self.logfile.flush()
        
    def getdir(self,log):
        pass
    
    def store(self, workspace,compressFileName,zipConstruct):
        '''
        for example:
        workspace is : ./results/
        compressFileName is :result.zip
        the directory of result.zip is ../results
        the result.zip's files construction is result.zip/Marble/marble.log
        '''
        #the zip file will up one level by results folder 
        resultzip = os.path.abspath(os.path.join(workspace,compressFileName))
        print 'compressing test results to %s' % resultzip
        preworkspace = os.path.abspath(os.getcwd())
        print 'current workspace is %s zipconstruct is %s' % (preworkspace,zipConstruct)
        with zipfile.ZipFile(resultzip, 'a') as myzip:
            print 'adding %s/%s' % (zipConstruct,self.filename)
            myzip.write(os.path.join(zipConstruct,self.filename))
        self.zipResult = resultzip
        self.logfile.close()

    def addfile(self, zipConstruct,filename,resultzip = None):
        '''
        zipconstruct is the relative directory about filename for current workspace
        '''
        preworkspace = os.path.abspath(os.getcwd())
        print 'current workspace is %s filename is %s' % (preworkspace,filename)
        
        if resultzip:
            print 'add %s to %s'%(filename, resultzip)
            with zipfile.ZipFile(resultzip, 'a') as myzip:
                myzip.write(os.path.join(zipConstruct,filename))
        elif self.zipResult:
            print 'add %s to %s'%(os.path.join(zipConstruct,filename), self.zipResult)
            with zipfile.ZipFile(self.zipResult, 'a') as myzip:
                myzip.write(os.path.join(zipConstruct,filename))
        else:
            print 'Please give the archive name'
class JsonItem(object):
    def __init__(self):
        self.parameters = ""
        self.itemType = None
        self.itemName = None
        
    def displayAttributes(self):
        for name, value in vars(self).items():
            print '%s = %s'%(name, value)
            
class TestTool(object):
    def __init__(self):
        self.name ='TestTool'
        self.resultdirs = 'results'
        self.logName = 'result.log'
        self.compressName = 'result.zip'
        self.workspace = os.path.abspath(os.getcwd())
        self.resultzip = os.path.join(self.workspace,self.compressName)
        self.currentProduct = None
        #fixed securityCode will store in seccode.txt
        self.securityCode = ''
        
    def _store(self,logger):
        logger.store(self.workspace,self.compressName,os.path.join(self.getResultdir(),self.name))

    def _parselog(self,destfile):
        junitparser = JunitParser()
        junitparser.parse(os.path.join(self.getResultdir(),destfile))

    def appendToArchive(self,filename):
        if self.resultzip:
            print 'add %s to %s'%(filename, self.resultzip)
            with zipfile.ZipFile(self.resultzip, 'a') as myzip:
                myzip.write(os.path.join(self.getResultdir(),filename))
        else:
            print 'can not found zip file'

    def _run(self, logger, toolArguments):

        command = self.getCommand(toolArguments)
        utilsHelper.runCommand(logger,command)

    def getCommand(self,toolArguments):
        command = 'adb %s' % toolArguments
        return command

    def getResultdir(self):
        return self.resultdirs
    def prepareLogger(self,resultdirs):
        if not os.path.exists(resultdirs):
            print 'make dirs %s'%resultdirs
            os.makedirs(resultdirs)
        return Logger(resultdirs,self.logName)

    def generatorLogfileName(self, testset):
        return "%s.log"%testset
