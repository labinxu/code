# coding -*- utf-8 _8-
import time


class AdbCommander(object):
    """
    ADB tool command
    """
    def __init__(self, utilsHelper):
        self.utilsHelper = utilsHelper

    def _cmdRootPhone(self, device):
        assert device is not None
        cmd = 'adb -s %s root' % device.sn
        return cmd

    def _cmdDumpsys(self, device, appstr):
        cmd = 'adb -s %s shell dumpsys %s'
        return cmd % (device.sn, appstr)

    def _cmdWaitfordevie(self, device):
        assert device is not None
        cmd = 'adb -s %s wait-for-device' % device.sn
        return cmd

    def _cmdSetlanguage(self, device, language):
        cmd = 'adb -s %s shell setprop persist.sys.language %s'
        return cmd % (device.sn, language)

    def _cmdGetLanguage(self, device):
        cmd = 'adb -s %s shell getprop persist.sys.language'
        return cmd % device.sn

    def _cmdSetCountry(self, device, country):
        cmd = 'adb -s %s shell setprop persist.sys.country %s'
        return cmd % (device.sn, country)

    def _cmdGetCountry(self, device):
        cmd = 'adb -s %s shell getprop persist.sys.country'
        return cmd % device.sn

    def _cmdRemoeDBLauncherMenu(self, device):
        rmDir = '/data/data/com.nokia.homescreen/databases/launcher_menu.db'
        cmd = 'adb -s %s shell rm -rf %s'
        return cmd % (device.sn, rmDir)

    def _cmdRemoeDBLauncherMenuJournal(self, device):
        rmDir = '/data/data/com.nokia.homescreen/databases/\
launcher_menu.db-journal'
        cmd = 'adb -s %s shell rm -rf %s'
        return cmd % (device.sn, rmDir)

    def _cmdReboot(self, device):
        cmd = 'adb -s %s reboot' % device.sn
        return cmd

    # ##########commander interfaces##############################
    # ############################################################
    def reboot(self, device):
        return self.utilsHelper.startProcess(self._cmdReboot(device))

    def dumpsysWindow(self, device):
        cmd = self._cmdDumpsys(device, 'window')
        ret, _ = self.utilsHelper.startProcessWithOutput(cmd)
        return ret

    def exceptSystemBooted(self, device, timeout=300):

        while 'mSystemBooted' not in self.dumpsysWindow(device) \
              and timeout > 0:

            time.sleep(5)
            timeout -= 5
        return timeout > 0

    def push(self, device, srcdir, destdir):
        cmd = 'adb -s %s push %s %s' % (device.sn, srcdir, destdir)
        return self.utilsHelper.startProcess(cmd)

    def getCountry(self, device):
        cmd = self._cmdGetCountry(device)
        stdout, _ = self.utilsHelper.startProcessWithOutput(cmd)
        return stdout

    def getLanguage(self, device):
        cmd = self._cmdGetLanguage(device)
        stdout, _ = self.utilsHelper.startProcessWithOutput(cmd)
        return stdout

    def rootPhone(self, device):
        cmd = self._cmdRootPhone(device)
        return self.utilsHelper.startProcess(cmd)

    def waitForDevice(self, device):
        cmd = self._cmdWaitfordevie(device)
        return self.utilsHelper.startProcess(cmd)

    def setlanguage(self, device, language):
        cmd = self._cmdSetlanguage(device, language)
        return self.utilsHelper.startProcess(cmd)

    def setcountry(self, device, country):
        cmd = self._cmdSetCountry(device, country)
        return self.utilsHelper.startProcess(cmd)

    def removeDBLauncherMenu(self, device):
        cmd = self._cmdRemoeDBLauncherMenu(device)
        return self.utilsHelper.startProcess(cmd)

    def removeDBLauncherMenuJournal(self, device):
        cmd = self._cmdRemoeDBLauncherMenuJournal(device)
        return self.utilsHelper.startProcess(cmd)

    def switchLanguage(self, device, language, country):
        '''
        switch the language
        '''
        # step one root phone
        self.rootPhone(device)

        # step two change language
        self.setlanguage(device, language)

        # step three change country
        self.setcountry(device, country)

        # step four remove db
        self.removeDBLauncherMenu(device)
        self.removeDBLauncherMenuJournal(device)

        # ########set screen time out ######################
        # ########################################################
    def _cmdSettingsDB(self, device, sqlstr):
        datadir = '/data/data'
        settingsDBDir = '/com.android.providers.settings/databases/settings.db'
        cmd = 'adb -s %s shell sqlite3 %s "%s"'
        return cmd % (device.sn, datadir+settingsDBDir, sqlstr)

    def setSreenTimeout(self, device, timeout):
        sqlstr = "update system set value='%s' where \
name='screen_off_timeout';" % timeout

        cmd = self._cmdSettingsDB(device, sqlstr)
        return self.utilsHelper.startProcess(cmd)

    def disableFirstTimeUse(self, product):
        cmd = 'adb -s %s shell pm disable com.nokia.FirstTimeUse/\
com.nokia.FirstTimeUse.LanguageSelection' % product.sn
        self.utilsHelper.startProcess(cmd)

        cmd = 'adb -s %s shell pm disable com.nokia.FirstTimeUse/\
com.nokia.FirstTimeUse.Warranty' % product.sn
        self.utilsHelper.startProcess(cmd)

        cmd = 'adb -s %s shell pm disable com.nokia.FirstTimeUse/\
com.nokia.FirstTimeUse.AccountCreation' % product.sn
        self.utilsHelper.startProcess(cmd)
