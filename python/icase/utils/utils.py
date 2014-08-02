# coding -*- utf-8 _8-

import glob
import os
import zipfile
import subprocess
import time
import shutil
import junit_parser
import datetime
from threading import Timer
# modules in same folder
from commandline import CommandLine
from adbcommander import AdbCommander


class Debug():
    '''
    Debug info print and write the log into files
    '''
    def __init__(self, logger=None, level=2):
        self.level = level
        self.logger = logger

    def formatLog(self, msg):
        '''
        Insert the time into line
        '''
        timeprefix = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return '[%s]%s' % (timeprefix, msg)

    def __call__(self, msg):
        self.debug(self.formatLog(msg))

    def debug(self, msg):
        msg = self.formatLog(msg)
        if self.level >= 3:
            print "Tool:Debug %s" % msg
        if self.logger:
            self.logger.append(msg)

    def info(self, msg):
        msg = self.formatLog(msg)
        if self.level >= 2:
            print "Tool:Info %s" % msg
        if self.logger:
            self.logger.append(msg)

    def error(self, msg):
        msg = self.formatLog(msg)
        if self.level >= 1:
            print "Tool:Error %s" % msg
        if self.logger:
            self.logger.append(msg)

    def output(self, msg):
        msg = self.formatLog(msg)
        print 'Tool:%s' % msg
        if self.logger:
            self.logger.append(msg)
debug = Debug(level=3)


class IcaseLogger(object):
    """save the output info into logfile

    """
    def __del__(self):
        self.log.close()

    def __init__(self, logfile):
        self.logfile = logfile
        logfile = os.path.abspath(logfile)
        if os.path.exists(logfile):
            self.log = open(logfile, 'a')
        else:
            self.log = open(logfile, 'w')

    def append(self, msg):
        if len(msg) == 0:
            return
        if msg[-1] != '\n':
            self.log.write('%s\n' % msg)
        else:
            self.log.write(msg)

        self.log.flush()


class Executor(object):
    def __init__(self, debug=None):
        self.debug = debug

    def executeWithOutput(self, command, timeout=None):
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        timer = None
        if timeout:
            self.debug.info('add timer %s' % str(timeout))
            kill_proc = lambda p: p.kill()
            timer = Timer(timeout, kill_proc)
            timer.start()
        stdoutdata, stderrdata = proc.communicate()
        if timer:
            timer.cancel()
            self.debug.output('cancel timer')

        return (stdoutdata, stderrdata)

    def setDebuger(self, debuger):
        self.debug = debuger

    def execute(self, command, timeout=None):

        self.debug.output('Execute %s' % command)
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        status = None
        t_beginning = time.time()
        while True:
            msg = proc.stdout.readline()
            status = proc.poll()
            if msg == '' and status is not None:
                break
            if msg != '':
                self.debug.output(msg)
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                self.debug.error('%s timeout' % command)
                break
        if status is None:
            # the process not finished
            status = proc.kill()
            self.debug.error('%s failed' % command)
        elif status == 0:
            self.debug.output('%s successful' % command)
        else:
            self.debug.error('%s error' % command)
        time.sleep(1)
        return status


class ExecuteException(Exception):
    '''
    Self exception class
    '''

    def __init__(self, msg=""):
        self.msg = msg

    def what(self):
        '''
        Return exception content
        '''
        return self.msg


class UtilsHelper():
    '''
    A single class contain flasher debug executor instance
    and provide interface to get it
    '''
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
        self.debug = Debug()
        self.executor = Executor(self.debug)
        self.wait_for_device = 'adb -s %s wait-for-device'
        self.dumpsys_window = 'adb -s %s shell dumpsys window'
        if not os.path.exists('results'):
            os.makedirs('results')

        self.commandLine = CommandLine(self)
        self.adbCommander = AdbCommander(self)

    def parseCmdLine(self):
        '''
        Get the command line from command input
        '''
        return self.commandLine.parseCmdLine()

    def getDevices(self, devicesJson):
        '''
        Get the device info from devices.json file
        '''
        import jsondata
        deviceparser = jsondata.DeviceParser(self, devicesJson)
        return deviceparser.getDevices()

    def getFlashArgs(self, cmdline):
        '''
        Retieve the flash args
        '''
        return self.commandLine.getFlashArgs(cmdline)

    def copyDeltaConfig(self):
        '''
        copy deltaConsoleFlash tools config file from
        path DELTA_FLASH to current directory
        '''

        deltaflashdir = os.environ.get('DELTA_FLASH')
        if deltaflashdir:
            self.debug.info(deltaflashdir)
            deltaflashdir = os.path.join(deltaflashdir, 'config.xml')
            if os.path.exists(deltaflashdir) and \
               not os.path.exists('config.xml'):
                shutil.copy(deltaflashdir, 'config.xml')
                return True
            else:
                self.debug.error("%s not found" % deltaflashdir)
        else:
            self.debug.error('DELTA_FLASH not found')
        return False

    def getDeviceDeltaType(self, product):
        '''
        Retieve the product type according the product anme
        '''
        deviceType = 'geminiplus'
        if product.productname in 'ara':
            deviceType = 'gemini'
        elif product.productname in 'athena':
            deviceType = 'geminiplus'
        else:
            deviceType = 'lyra'
        return deviceType

    def pingDevice(self, product):
        '''
        Send data to phone ,if the phone start normal
        it will response
        '''
        param = '00,00,10,15,00,06,00,00,00,02,00,00'
        self.debug.info('ping devie...')
        ping = 'DeltaConsoleFlasher send -s \
%s -i %s -e %s' % (param, product.imei, self.getDeviceDeltaType(product))

        success = 'RX:'
        counter = 30
        while counter > 0:
            stdout, _ = self.startProcessWithOutput(ping)
            if success in stdout:
                self.debug.info(stdout)
                return True
            else:
                counter -= 1
                time.sleep(10)
        return False

    def activeUsb(self, product):
        '''
        Make the use debug mode active
        '''
        param = '00,00,10,1b,00,06,00,01,04,35,00,00'
        active_usb = 'DeltaConsoleFlasher send -s \
%s -i %s -e %s' % (param, product.imei, self.getDeviceDeltaType(product))
        stdout, _ = self.startProcessWithOutput(active_usb)
        success = 'RX:'
        if success in stdout:
            self.debug.info(stdout)
            return True
        else:
            return False

    def getFlasher(self, product, flashTool='fastboot'):
        '''
        Retrieve the flash tool according to param flashtool
        '''
        from flasher import AdbFlasher, DeltaFlasher
        if 'fastboot' in flashTool:
            self.flasher = AdbFlasher(self, product)
        elif 'delta' in flashTool:
            self.flasher = DeltaFlasher(self, product)
        else:
            self.flasher = AdbFlasher(self, product)
        self.copyDeltaConfig()
        return self.flasher

    def findFirstFile(self, filereg):
        '''
        Retrieve the files use glob module
        '''

        self.debug('finding file %s' % filereg)
        files = glob.glob(filereg)
        retfile = ''
        if len(files) == 0:
            self.debug.info('%s not found' % filereg)
            return None
        else:
            retfile = files[0]
            self.debug.info('find file %s' % retfile)

        return retfile

    def waitSystemStart(self, product, timeout=90):
        '''
        Wait the phone startup ,using dumpsys window command
        '''
        self.debug.output('waiting system starting...')
        ret = self.adbCommander.exceptSystemBooted(product)
        if ret:
            time.sleep(timeout)
        return ret

    def setLogger(self, logger):
        if not self.debug:
            self.debug = Debug(logger)
        else:
            self.debug.logger = logger
        self.executor.setDebuger(self.debug)

    def getLastError(self):
        return self.executeStates

    def debug(self, msg):
        self.debug.debug(msg)

    def startProcessWithOutput(self, command, timeout=None, report=True):
        if report:
            self.debug.output(command)

        return self.executor.executeWithOutput(command, timeout=timeout)

    def startProcess(self, command, timeout=None):
        self.executeStates = self.executor.execute(command, timeout)
        return self.executeStates

    def raiseException(self, msg=None):
        '''
        '''
        if os.path.exists('./results'):
            with open('./results/error.log', 'w') as f:
                f.write(msg)
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

    def runCommand(self, logger, command, timeout=None):
        self.setLogger(logger)
        return self.executor.execute(command, timeout=timeout)

    def setWorkspace(self, new_workspace):
        self.workspace = new_workspace

    def checkLanguage(self, product, language):
        result = self.adbCommander.getLanguage(product)
        if language in result:
            self.debug.info('switch language successful')
            return True
        else:
            self.debug.error('switch language failed')
            return False

    def switchLanguage(self, product, language, country):
        self.adbCommander.switchLanguage(product, language, country)

    def rebootTarget(self, product):
        self.adbCommander.reboot(product)
        time.sleep(10)
        self.adbCommander.waitForDevice(product)
        if not self.waitSystemStart(product):
            return False
        return True

    def setSreenTimeout(self, product, timeout='1800000'):

        return self.adbCommander.setSreenTimeout(product, timeout)

    def disableFirstTimeUse(self, product):
        return self.adbCommander.disableFirstTimeUse(product)

    def installTesthelper(self, product):
        self.debug.info('Enter install test helper')
        directory = './utils/TestHelpers.jar'
        if os.path.exists(directory):
            return self.adbCommander.push(product, directory,
                                          '/data/local/tmp')
        else:
            self.debug.error('%s not exist' % directory)

    def setSimOnline(self, product):

        securityCode = self.getSecurityCode(product.productname)

        cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c \
com.testhelpers.DeviceUnlock -e securitycodes %s' % (product.sn, securityCode)
        self.executor.execute(cmd, timeout=30)
        time.sleep(5)

        cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c \
com.testhelpers.GetSIMsOnline#getDualSIMsOnline' % product.sn

        self.executor.execute(cmd, timeout=30)
        time.sleep(5)

        cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c \
com.testhelpers.GetSIMsOnline#setNetworkMode' % product.sn
        self.executor.execute(cmd, timeout=30)
        time.sleep(5)

    def clearsdcard1(self, product):
        cmd = 'adb -s %s root' % product.sn
        self.executor.execute(cmd, timeout=30)

        cmd = 'adb -s %s shell rm -rf /storage/sdcard1/*' % product.sn
        self.executor.execute(cmd, timeout=30)

    def simCardInit(self, product):
        '''run adb command to enable dual sim card
        '''
        cmd = 'adb -s %s shell setprop \
persist.radio.multisim.config dsds' % product.sn
        if product.simcount == 2:
            self.executor.execute(cmd, timeout=30)

    def unlockPhone(self, logger, product):

        securityCode = self.getSecurityCode(product.productname)

        cmd = 'adb -s %s shell uiautomator runtest TestHelpers.jar -c \
com.testhelpers.DeviceUnlock -e securitycodes %s' % (product.sn, securityCode)
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

    def _parselog(self, destfile):
        junitparser = JunitParser()
        junitparser.parse(os.path.join(self.getResultdir(), destfile))

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
        return IcaseLogger(os.path.join(resultdirs, self.logName))

    def generatorLogfileName(self, testset):
        return "%s.log" % testset
