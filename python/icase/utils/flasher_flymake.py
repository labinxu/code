# coding -*- utf-8 _8-

import os
import time
import xml.etree.ElementTree as ET


class Flasher(object):
    '''
    Base of flash classes
    '''

    def __init__(self, utilsHelper, product):
        self.utilsHelper = utilsHelper
        self.product = product
        self.flash_files = {}

    def setFlashFiles(self, files):
        '''
        Specified the flash files of the partition
        '''
        self.flash_files = files

    def makeFlashCmd(self, param=''):
        pass

    def copyAdbKey(self):
        """
        copyAdbKey. Returns True if success, False in failure.
        Keyword arguments:
        verbose - True to enable traces (False by default)
        """
        Cmd = self.getCopyAdbkeyCmd()
        self.utilsHelper.startProcess(Cmd)
        return self.utilsHelper.executeStates == 0

    def getCopyAdbkeyCmd(self):
        '''
        Copy the adbkey.pub file from home directory to phone sdcard
        '''

        userHome = ''
        if os.environ.get('USERPROFILE'):
            userHome = os.environ['USERPROFILE'].encode('string-escape')
        else:
            self.utilsHelper.raiseException('not found USERPROFILE')
        pubkey = os.path.join(userHome, '.android', 'adbkey.pub')
        # pubkey = userHome + os.sep + '.android' + os.sep + 'adbkey.pub'
        if os.path.exists(pubkey):
            Cmd = 'adb -s %s push %s /storage/sdcard1/adb_keys' %\
                  (self.product.sn, pubkey)
        else:
            self.utilsHelper.debug.error('Can not found %s' % pubkey)
            Cmd = None
        return Cmd


class DeltaFlasher(Flasher):
    """
    Use the deltaConsoleFlasher to flash phone
    """
    def __init__(self, utilsHelper, product):
        Flasher.__init__(self, utilsHelper, product)
        self.deviceType = None
        self.flashCmd = None
        if product.productname in 'ara':
            self.deviceType = 'gemini'
        elif product.productname in 'athena':
            self.deviceType = 'geminiplus'
        else:
            self.deviceType = 'lyra'

        self.setupConfig = 'DeltaConsoleFlasher scan -e %s' % self.deviceType

        self.setTestMode = 'DeltaConsoleFlasher setMode -e %s \
-m Test -i %s' % (self.deviceType, product.imei)

        self.setNormalMode = 'DeltaConsoleFlasher setMode -e %s \
-m Normal -i %s' % (self.deviceType, product.imei)

    def getImeis(self, conf='config.xml'):
        '''
        Read the imeis from config.xml which created by
        DeltaConsoleFlasher scan -e ..
        '''

        imeis = []
        if os.path.exists(conf):
            doc = ET.parse(conf)
            root = doc.getroot()
            self.utilsHelper.debug.info('read imei from config')
            for devices in root.findall('devices'):
                for device in devices.findall('device'):
                    imeis.append(device.get('imei'))
        else:
            self.utilsHelper.debug.error('%s not found' % conf)
        return imeis

    def changeTestMode(self):
        '''
        change the phone to test mode
        '''
        stdout, _ = self.utilsHelper.startProcessWithOutput(self.setTestMode)
        return stdout

    def changeNormalMode(self):
        stdout, _ = self.utilsHelper.startProcessWithOutput(self.setNormalMode)
        return stdout

    def makeFlashCmd(self, findfile='*.vpl'):
        '''
        Generate delta flash command line
        '''

        vplfile = self.utilsHelper.findFirstFile(findfile)

        self.flashCmd = 'DeltaConsoleFlasher flash -e %s -v %s \
-i %s' % (self.deviceType, vplfile, self.product.imei)

        return self.flashCmd

    def startflash(self, timeout=None):
        # change device  to test mode
        # set up config
        return self.copyAdbKey()

    def flash(self, steptimeout=None, totalTimeout=None):
        self.makeFlashCmd('./*.vpl')
        if not self.startflash():
            return False

        if self.flashCmd:
            self.utilsHelper.startProcess(self.flashCmd)
            if not self.utilsHelper.executeStates == 0:
                return False
        else:
            self.utilshelper.raiseException('make flash cmd failed')

        return self.utilsHelper.executeStates == 0

    def endFlash(self):
        if not self.utilsHelper.pingDevice(self.product):
            self.utilsHelper.debug.error('Ping %s failed' % self.product.imei)
        self.utilsHelper.activeUsb(self.product)


class AdbFlasher(Flasher):
    """The fasttool to flash phone
    """

    def __init__(self, utilsHelper, product=None):
        Flasher.__init__(self, utilsHelper, product)
        if product:
            self.beginFlash = 'adb -s %s reboot bootloader' % self.product.sn
            self.reboot = 'fastboot -s %s reboot' % self.product.sn
        self.defaultTimeout = 10
        self.flashdir = './flash'

    def getFlashConfName(self):
        '''
        Get the flash config file from the default directory
        by product name and product's hardware type
        '''

        if self.product and self.product.productname \
           and self.product.hwtype:

            return "%s_%s.xml" % (self.product.productname,
                                  self.product.hwtype)
        else:
            return None

    def getFlashConf(self, conffile='./flash/hwflash.xml'):
        '''
        Parse the configure file and retrieve the
        flash partions name and is according files
        '''
        if not os.path.exists(conffile):
            return []

        import xml.etree.ElementTree as ET

        doc = ET.parse(conffile)
        root = doc.getroot()
        confs = []

        for item in root.findall('item'):
            partionName = item.get('name')
            self.utilsHelper.debug('partionName %s' % partionName)
            if partionName in self.flash_files.keys():
                findfile = self.flash_files[partionName]
                flashfile = self.utilsHelper.findFirstFile(findfile)
            else:
                findfile = item.find('value').text
                flashfile = self.utilsHelper.findFirstFile(findfile)
                if not flashfile:
                    backup = item.find('backup')
                    if backup is not None:
                        findfile = backup.text
                        flashfile = self.utilsHelper.findFirstFile(findfile)

            option = item.get('option')
            if flashfile:
                confs.append((partionName, flashfile, option))
            elif 'mandatory' in option:
                self.utilsHelper.debug.error('%s not found' % findfile)
                return None
        return confs

    def startflash(self):
        self.copyAdbKey()
        self.utilsHelper.startProcess(self.beginFlash)
        time.sleep(10)
        checkfastboot = 'fastboot -s %s devices' % self.product.sn
        stdout, stderr = self.utilsHelper.startProcessWithOutput(checkfastboot)
        counter = 3
        while self.product.sn not in stdout and counter > 0:
            time.sleep(10)
            stdout, stderr = self.utilsHelper.startProcessWithOutput(checkfastboo)
            counter -= 1

        if self.utilsHelper.executeStates != 0:
            return self.utilsHelper.executeStates
        time.sleep(self.defaultTimeout)

        return self.utilsHelper.executeStates

    def flash(self, steptimeout=None, totalTimeout=None):
        '''
        flash phone
        '''
        # self.utilsHelper.runCommand()
        msg = 'Flash %s %s' % (self.product.productname, self.product.hwtype)
        self.utilsHelper.debug.info(msg)
        flashconffile = self.getFlashConfName()
        if flashconffile:
            flashconffile = os.path.join(self.flashdir, flashconffile)
            if os.path.exists(flashconffile):
                msg = 'Use hwconf %s' % flashconffile
                self.utilsHelper.debug.output(msg)
            else:
                msg = 'can not found %s ,check devices.json' % flashconffile
                self.utilsHelper.debug.info(msg)
                msg = 'using defult hwconf file ./flash/hwflash.xml'
                self.utilsHelper.debug.info(msg)

                flashconffile = './flash/hwflash.xml'
        else:
            msg = 'useing default hwconf %s ,check devices.json'
            self.utilsHelper.debug.info(msg)
            flashconffile = './flash/hwflash.xml'

        self.flashCmds = self.getFlashConf(flashconffile)
        if not self.flashCmds:
            self.utilsHelper.debug.error('flash command error')
            return False

        if self.startflash() != 0:
            msg = 'failed status %s' % self.utilsHelper.executeStates
            self.utilsHelper.debug.error(msg)

        cmds = self.getFlashCmds(self.flashCmds)
        for cmd in cmds:
            if self.utilsHelper.startProcess(cmd, timeout=steptimeout) != 0:
                self.utilsHelper.debug.error('%s failed' % cmd)
                return False

        return self.endFlash()

    def getFlashCmds(self, flashCmds):
        '''
        Generate flash command base on the config file
        '''
        cmds = []
        for partion, arg, _ in flashCmds:
            tmpparam = (self.product.sn, partion, arg)
            if partion == 'system':
                cmd = 'fastboot -s %s -S 200M flash %s %s' % tmpparam
            else:
                cmd = 'fastboot -s %s flash %s %s' % tmpparam
            cmds.append(cmd)
        return cmds

    def endFlash(self):
        '''
        Restart phone after flash phone success
        '''

        self.utilsHelper.startProcess(self.reboot)
        time.sleep(self.defaultTimeout)
        if not self.utilsHelper.pingDevice(self.product):
            self.utilsHelper.debug.error('ping %s failed' % self.product.imei)
        self.utilsHelper.activeUsb(self.product)

        if not self.utilsHelper.waitSystemStart(self.product):
            return False
        else:
            time.sleep(self.defaultTimeout)
            return True
