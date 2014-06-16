import os
import zipfile
import subprocess
import time
import sys
import threading
import shutil
import junit_parser


class Debug():

    def __init__(self, logger=None, level=2):
        self.level = level
        self.logger = logger

    def debug(self, msg):
        if self.level >= 3:
            print "Tool: Debug %s" % msg
        if self.logger:
            self.logger.writeLine(msg)

    def info(self, msg):
        if self.level >= 2:
            print "Tool: Info %s" % msg
        if self.logger:
            self.logger.writeLine(msg)

    def error(self, msg):
        if self.level >= 1:
            print "Tool: Error %s" % msg
        if self.logger:
            self.logger.writeLine(msg)

    def output(self, msg):
        print 'Tool: %s' % msg
        if self.logger:
            self.logger.writeLine(msg)

debug = Debug(level=3)


class IcaseLogger(object):
    """save the output info into logfile

    """
    def __del__(self):
        self.log.close()

    def __init__(self, logfile):
        self.logfile = logfile
        if os.path.exists(logfile):
            self.log = open(logfile, 'a')
        else:
            print os.path.abspath(logfile)
            self.log = open(logfile, 'w')

    def writeLine(self, msg):
        self.log.write(msg)
        self.log.flush()


class Executor(object):
    def __init__(self, debug=None):
        self.debug = debug

    def execute(self, command, timeout=None):
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        status = None
        while True:
            msg = proc.stdout.readline()
            time.sleep(1)
            status = proc.poll()
            if msg == '' and status is not None:
                break
            self.debug.output(msg)

            if timeout is not None:
                timeout -= 1
                if timeout <= 0:
                    self.debug.error('cmd %s timout' % command)
                    break

        if status is None:
            # the process not finished
            status = proc.kill()
            self.debug.error('cmd %s failed' % command)
        elif status == 0:
            self.debug.output('cmd %s successful' % command)

        return status


class Flasher(object):
    """The flash command inclued
    """

    def __init__(self, utilsHelper, productSN):
        self.utilsHelper = utilsHelper
        self.productSN = productSN
        self.beginFlash = 'adb -s %s reboot bootloader' % self.productSN
        self.reboot = 'fastboot -s %s reboot' % self.productSN
        self.flashCmds = []
        self.flashCmds.append(('modem', '*Non-HLOS.bin'))
        self.flashCmds.append(('sbl1', '*sbl1'))
        self.flashCmds.append(('sbl1bak', '*sbl1'))
        self.flashCmds.append(('rpm', '*rpm.mbn'))
        self.flashCmds.append(('rpmbak', '*rpm.mbn'))
        self.flashCmds.append(('tz', '*tz.mbn'))
        self.flashCmds.append(('tzbak', '*tz.mbn'))
        self.flashCmds.append(('aboot', '*emmc_appsboot.mbn'))
        self.flashCmds.append(('abootbak', '*emmc_appsboot.mbn'))
        self.flashCmds.append(('boot', '*boot.img'))
        self.flashCmds.append(('system', '*system.img'))
        self.flashCmds.append(('cache', '*cache.img'))
        self.flashCmds.append(('userdata', '*userdata.img'))
        self.flashCmds.append(('recovery', '*recovery.img'))
        # self.flashCmds.append(('custom', '*custom.img'))
        self.flashCmds.append(('custom', self.getCustomImg()))

        self.flashCmds.append(('sdi', '*sdi.mbn'))

    def startflash(self):
        utilsHelper.startProcess(self.beginFlash)

    def getCustomImg(self):
        import glob
        coustom = glob.glob('rm*.*custom.img')
        assert len(coustom) > 1
        print len(coustom)
        return coustom[0]

    def flash(self, steptimeout=None, totalTimeout=None):
        # self.utilsHelper.runCommand()
        self.startflash()

        for partion, arg in self.flashCmds:
            tmpparam = (self.productSN, partion, arg)
            if partion == 'system':
                cmd = 'fastboot -s %s -S 200M flash %s %s' % tmpparam
            else:
                cmd = 'fastboot -s %s flash %s %s' % tmpparam
            if self.utilsHelper.startProcess(cmd) != 0:
                pass
        self.endFlash()

    def endFlash(self):
        utilsHelper.startProcess(self.reboot)


class CommandWatchCat(threading.Thread):
    def __init__(self, popen, timeout):
        threading.Thread.__init__(self)
        self.popen = popen
        self.timeout = timeout

    def run(self):

        tmptimeout = self.timeout
        status = self.popen.poll()
        while tmptimeout is not 0 and status is None:
            tmptimeout -= 1
            time.sleep(1)
            status = self.popen.poll()

        status = self.popen.poll()
        if status is None:
            self.popen.kill()
            print 'kill process reason timeout'
            # wait the process return
            tmptimeout = self.timeout
            while status is None and tmptimeout is not 0:
                time.sleep(1)
                tmptimeout -= 1
                self.popen.kill()
                status = self.popen.poll()


class ExecuteException():
    def __init__(self, msg=""):
        self.msg = msg

    def what(self):
        return self.msg


class UtilsHelper():

    def __init__(self):
        self.testMode = False
        import platform
        if platform.system() == 'Windows':
            self.isWindows = True
        else:
            self.isWindows = False

        self.workspace = os.path.abspath(os.getcwd())
        self.resultName = None
        self.executeStates = 0

        self.logger = IcaseLogger('./results/icase.log')
        self.debug = Debug(self.logger)
        self.executor = Executor(debug)

    def setLogger(self, logger):
        self.logger = logger
        self.debug.logger = self.logger

    def getLastError(self):
        return self.executeStates

    def debug(self, msg):
        self.debug.debug(msg)

    def startProcess(self, command, timeout=None):
        if self.testMode:
            print 'cmd:', command
            return 0
        else:
            self.executeStates = self.executor.execute(command, timeout)
            return self.executeStates

    def raiseException(self, msg=None):
        raise ExecuteException(msg)

    def getDataFromInfofile(self, file):
        data = {}
        with open(file, 'r') as f:
            for line in f.readlines():
                if line == '\n':
                    debug.info('empty')
                    continue
                line = line.replace("'", "")
                line = line[0:-1]
                vars = line.split('=')
                size = len(vars)
                if size == 2:
                    # parse the second level
                    data[vars[0]] = vars[1]
                    #
                elif size == 3:
                    temp = {}
                    temp[vars[1]] = vars[2]
                    data[vars[0]] = temp
        return data

    def copytree(self, src, dst, symlinks=False):
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

    def copyFolderContents(self, src, dest):
        '''
        replace the files if it exist
        '''
        for item in os.listdir(src):
            if os.path.isdir(os.path.join(src, item)):
                self.copytree(os.path.join(src, item),
                              os.path.abspath(os.path.join(dest, item)))
                srcdir = os.path.abspath(os.path.join(src, item))
                desdir = os.path.abspath(os.path.join(dest, item))
                print 'copy %s to %s' % (srcdir, desdir)
            elif os.path.isfile(os.path.join(src, item)):
                shutil.copy(os.path.join(src, item), dest)
                srcdir = os.path.abspath(os.path.join(src, item))
                desdir = os.path.abspath(dest)
                print 'copy %s to %s' % (srcdir, desdir)

    def runCommand2(self, command, timeout=None):

        self.executeStates = 0
        try:
            print 'run %s' % command
            tool = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            # create a command watch cat
            if timeout:
                CommandWatchCat(tool, timeout=timeout).start()
            toolOutputs = tool.stdout
            while 1:
                outputFromTool = toolOutputs.readline()
                time.sleep(1/10)
                if not outputFromTool:
                    break
                print 'Tool: ' + outputFromTool
            self.executeStates = tool.wait()
            print 'process return %d' % self.executeStates
        except OSError, e:
            print 'An error occured during execution: ', e
        sys.stdout = sys.__stdout__
        return self.executeStates

    def waitDeviceStart(self, logger, sn):
        debug.debug('wait for device startup')
        cmd = 'adb -s %s wait-for-device' % sn
        utilsHelper.runCommand2(cmd, timeout=300)
        cmd = 'adb -s %s shell dumpsys window' % sn
        counter = 12
        debug.debug('checking phone status...')
        while counter > 0:
            counter -= 1
            try:
                params = 'SystemBooted=true'
                (states, ret) = utilsHelper.runCommandAndExcept(cmd, params)
                print 'states', states
                if ret:
                    debug.debug('start up')
                    return True
                time.sleep(10)
            except Exception, e:
                debug.error(e)
        return False

    def runCommandAndExcept(self, command, exceptstr=None):
        try:
            findstr = False
            print 'run %s' % command
            tool = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            toolOutputs = tool.stdout
            while 1:
                outputFromTool = toolOutputs.readline()
                time.sleep(1)
                if not outputFromTool:
                    break

                if exceptstr and exceptstr in outputFromTool:
                    findstr = True
                    break
                print 'Tool: ' + outputFromTool
        except Exception, e:
            debug.error(e)

        return (self.executeStates, findstr)

    def runCommand(self, logger, command,
                   timeout=None,
                   interval=None,
                   repeat=3,
                   report=True):

        self.executeStates = 0
        assert repeat is not 0

        try:
            counter = repeat
            while(counter > 0):
                print 'run %s' % command
                tool = subprocess.Popen(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
                # create a command watch cat
                if timeout:
                    CommandWatchCat(tool, timeout=timeout).start()
                    if not interval:
                        interval = timeout / repeat
                toolOutputs = tool.stdout
                while 1:
                    outputFromTool = toolOutputs.readline()
                    time.sleep(0.5)
                    if not outputFromTool:
                        break
                    if report:
                        print 'Tool: ' + outputFromTool
                    logger.append(outputFromTool)
                self.executeStates = tool.wait()
                print 'process return %d,counter %d' %\
                    (self.executeStates, counter)
                if self.executeStates != 0 and timeout:
                    print 'Tool: command %s faild try it after %s' %\
                        (command, str(interval))
                    counter -= 1
                    time.sleep(interval)
                else:
                    print 'Tool: command %s finished' % command
                    counter = 0

                sys.stdout = sys.__stdout__
        except OSError, e:
            sys.stdout = sys.__stdout__
            print 'An error occured during execution: ', e
        return self.executeStates

    def setWorkspace(self, new_workspace):
        self.workspace = new_workspace

    def SwitchPhoneLanguage(self, logger, product, language, country):
        print 'switch phone language to %s and country to %s' %\
            (language, country)
        cmd = 'adb -s %s root' % product.sn
        self.runCommand(logger, cmd, timeout=30)
        cmd = 'adb -s %s wait-for-device' % product.sn
        self.runCommand(logger, cmd, timeout=30)
        cmd = 'adb -s %s shell setprop persist.sys.language %s' %\
              (product.sn, language)
        self.runCommand(logger, cmd, timeout=30)
        cmd = 'adb -s %s shell setprop persist.sys.country %s' %\
              (product.sn, country)
        self.runCommand(logger, cmd, timeout=30)
        cmd = 'adb -s %s shell rm -rf /data/data/com.nokia.homescreen/databases/launcher_menu.db' % product.sn
        self.runCommand(logger, cmd, timeout=30)
        cmd = 'adb -s %s shell rm -rf /data/data/com.nokia.homescreen/databases/launcher_menu.db-journal' % product.sn
        self.runCommand(logger, cmd, timeout=30)
        cmd = 'adb -s %s reboot' % product.sn
        self.runCommand(logger, cmd, timeout=30)
        print 'set finished and reboot'
        cmd = 'adb -s %s wait-for-device' % product.sn
        self.runCommand(logger, cmd, timeout=300)
        print 'device is online again'
        if not self.waitDeviceStart(logger, product.sn):
            debug.info('startup timeout reboot and wait again')
            cmd = 'adb -s %s reboot' % product.sn
            self.runCommand(logger, cmd, timeout=30)
            if not self.waitDeviceStart(logger, product.sn):
                self.raiseException('phone can not startup')

        print 'reboot finished'

    def installTesthelper(self, product):
        print 'Enter install test helper'
        directory = os.path.join(self.workspace, 'utils', 'TestHelpers.jar')
        if os.path.exists(os.path.join(self.workspace, 'utils',
                                       'TestHelpers.jar')):

            if not os.path.exists('results'):
                os.makedirs('results')

            logger = Logger('results', 'flash.log')

            cmd = 'adb -s %s push %s /data/local/tmp' % (product.sn, directory)
            self.runCommand(logger, cmd, timeout=30)

            cmd = 'adb -s %s shell pm disable com.nokia.FirstTimeUse/com.nokia.FirstTimeUse.LanguageSelection'%product.sn
            self.runCommand(logger, cmd, timeout=30)
            cmd ='adb -s %s shell pm disable com.nokia.FirstTimeUse/com.nokia.FirstTimeUse.Warranty'%product.sn
            self.runCommand(logger, cmd, timeout=30)

            cmd = 'adb -s %s root' % product.sn
            self.runCommand(logger, cmd, timeout=30)
            cmd = 'adb -s %s shell rm -rf /storage/sdcard1/*' % product.sn
            self.runCommand(logger, cmd, timeout=30)

            # =====run adb command to enable dual sim card==========
            cmd = 'adb -s %s shell setprop persist.radio.multisim.config dsds'\
                  % product.sn
            if product.simcount == 2:
                self.runCommand(logger, cmd)

            self.SwitchPhoneLanguage(logger, product, 'en', 'US')
            # cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c com.testhelpers.DeviceInitialization -e timeout 500' % product.sn
            # self.runCommand(logger,cmd,timeout=500)
        
    def unlockPhone(self, logger, product):
        securityCode = self.getSecurityCode(product.productName)
        cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c com.testhelpers.DeviceUnlock -e securitycodes %s' % (product.sn, securityCode)
        self.runCommand(logger, cmd, timeout=60)

    def addDirArchive(self, archiveName, startdir):

        print 'add %s to %s' % (startdir, archiveName)
        with zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED) as f:
            for dirpath, dirnames, filenames in os.walk(startdir):
                for filename in filenames:
                    print 'add %s' % (os.path.join(dirpath, filename))
                    f.write(os.path.join(dirpath, filename))

    def addArchive(self, archiveName, filename):
        print 'add %s to %s' % (archiveName, filename)
        with zipfile.ZipFile(archiveName, 'a') as myzip:
            myzip.write(filename)

    def getSecurityCode(self, productName):
        print 'open %s' % os.path.join(self.workspace, 'utils/seccode.txt')
        with open(os.path.join(self.workspace, 'utils/seccode.txt')) as f:
            for line in f.readlines():
                if productName in line:
                    return line.split('=')[1]
        return None

    def addArchives(self, archiveName, files):
        with zipfile.ZipFile(archiveName, 'a') as myzip:
            for file in files:
                print 'add %s to %s' % (archiveName, file)
                myzip.write(file)

    def findfiles(self, targetdirectory):
        results = []
        for root, dirs, files in os.walk(targetdirectory):
            for fn in files:
                results.append(os.path.join(root, fn))
        return results

    def parseCmdLine(self):
                
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-p', '--product', dest='product',
                          help='contains product information')
        parser.add_option('-f', '--flash', dest='flash',
                          help='flash tool name and path')
        
        parser.add_option('-T', '--testtype', dest='testtype',
                          help='type of the test eg: \
marble,instrument,Monkey...')
        
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
        parser.add_option('-R' ,'--result',dest = 'result',help='result zip name')
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

    def parse(self, destfile):
        junit_parser.parse(destfile)


class Logger:
    def __init__(self, dir, logfile):
        self.filename = logfile
        self.logpath = os.path.abspath(os.path.join(dir, logfile))
        if os.path.exists(self.logpath):
            self.logfile = open(self.logpath, 'a')
        else:
            self.logfile = open(os.path.abspath(os.path.join(dir, logfile)),
                                'w')
        self.workspace = dir
        self.zipResult = None

    def append(self, log):
        self.logfile.write(log)
        self.logfile.flush()

    def find(self, destStr):
        with open(self.logpath, 'r') as f:
            for line in f.readlines():
                if destStr in line:
                    return line
        return None

    def store(self, workspace, compressFileName, zipConstruct):
        '''
        for example:
        workspace is : ./results/
        compressFileName is :result.zip
        the directory of result.zip is ../results
        the result.zip's files construction is result.zip/Marble/marble.log
        '''
        # the zip file will up one level by results folder
        resultzip = os.path.abspath(os.path.join(workspace, compressFileName))
        print 'compressing test results to %s' % resultzip
        with zipfile.ZipFile(resultzip, 'a') as myzip:
            print 'adding %s/%s' % (zipConstruct, self.filename)
            myzip.write(os.path.join(zipConstruct, self.filename))
        self.zipResult = resultzip
        self.logfile.close()

    def addfile(self, zipConstruct, filename, resultzip=None):
        '''
        zipconstruct is the relative directory
        about filename for current workspace
        '''

        if resultzip:
            print 'add %s to %s' % (filename, resultzip)
            with zipfile.ZipFile(resultzip, 'a') as myzip:
                myzip.write(os.path.join(zipConstruct, filename))
        elif self.zipResult:
            print 'add %s to %s' % (os.path.join(zipConstruct, filename),
                                    self.zipResult)
            with zipfile.ZipFile(self.zipResult, 'a') as myzip:
                myzip.write(os.path.join(zipConstruct, filename))
        else:
            print 'Please give the archive name'


class JsonItem(object):
    def __init__(self):
        self.parameters = ""
        self.itemType = None
        self.itemName = None
        
    def displayAttributes(self):
        for name, value in vars(self).items():
            print '%s = %s' % (name, value)


class TestTool(object):
    def __init__(self):
        self.name = 'TestTool'
        self.resultdirs = 'results'
        self.logName = 'result.log'
        self.compressName = utilsHelper.resultName
        self.workspace = os.path.abspath(os.getcwd())
        self.resultzip = os.path.join(self.workspace, self.compressName)
        self.currentProduct = None
        # fixed securityCode will store in seccode.txt
        self.securityCode = ''
        
    def _store(self, logger):

        logger.store(self.workspace, self.compressName,
                     os.path.join(self.getResultdir(), self.name))

    def _parselog(self, destfile):
        junitparser = JunitParser()
        junitparser.parse(os.path.join(self.getResultdir(), destfile))

    def appendToArchive(self, filename):
        if self.resultzip:
            print 'add %s to %s' % (filename, self.resultzip)
            with zipfile.ZipFile(self.resultzip, 'a') as myzip:
                myzip.write(os.path.join(self.getResultdir(), filename))
        else:
            print 'can not found zip file'

    def _run(self, logger, toolArguments):

        command = self.getCommand(toolArguments)
        utilsHelper.runCommand(logger, command)

    def getCommand(self, toolArguments):
        command = 'adb %s' % toolArguments
        return command

    def getResultdir(self):
        return self.resultdirs

    def prepareLogger(self, resultdirs):
        if not os.path.exists(resultdirs):
            print 'make dirs %s' % resultdirs
            os.makedirs(resultdirs)
        return Logger(resultdirs, self.logName)

    def generatorLogfileName(self, testset):
        return "%s.log" % testset
