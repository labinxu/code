# coding -*- utf-8 _8-
import datetime
import sys
import os
import unittest as UT

if '../' not in sys.path:
    sys.path.append('../')
from utils.utils import utilsHelper, IcaseLogger

if not os.path.exists('results'):
    os.makedirs('results')


logger = IcaseLogger('./results/flash.log')
utilsHelper.setLogger(logger)
FLASH = False


class Icase_test_suits(UT.TestCase):

    def setUp(self):

        self.utilsHelper = utilsHelper

        class Product:
            def __init__(self):
                self.productname = 'athena'
                self.imei = 'imeiimei'
                self.sn = 'snsnsns'

        self.product = Product()
        self.product.imei = '0044024786619560'
        self.product.productName = 'athena'
        self.product.sn = 'ff0acb'
        utilsHelper.resultName = 'result.zip'

    def testFormatTime(self):
        # print time.strftime('%H:%M:%S', time.localtime(time.time()))
        now = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.assertEqual(len(now), 12)
    
    def testUtilsDebugprint(self):
        self.utilsHelper.debug.output('test output')

    def testUtilsHelperFindfiles(self):

        file = self.utilsHelper.findFirstFile('../flash/OLD-NON-HLOS.bin')
        self.assertTrue('OLD-NON-HLOS' in file)

    def test_flasher_getFlashConf(self):
        flasher = self.utilsHelper.getFlasher(self.product)
        confs = flasher.getFlashConf()
        l = [partition for partition, file, _ in confs]
        self.assertTrue('sdi' not in l)

    def test_flasher_getflashcmds(self):
        flasher = self.utilsHelper.getFlasher(self.product)
        # confs1 = flasher.getFlashConf('../flash/athena_B1.xml')

        # cmds1 = flasher.getFlashCmds(confs1)
        # self.assertTrue(len(cmds1) == len(confs1))
        # confs2 = flasher.getFlashConf('../flash/athena_S0.2.xml')
        # cmds2 = flasher.getFlashCmds(confs2)
        # self.assertTrue(len(cmds2) == len(confs2))

        # confs3 = flasher.getFlashConf('../flash/athena_S1.1.xml')
        # cmds3 = flasher.getFlashCmds(confs3)
        # self.assertTrue(len(cmds3) == len(confs3))

        confs4 = flasher.getFlashConf('../flash/libralte_B1.xml')
        cmds4 = flasher.getFlashCmds(confs4)
        self.assertTrue(len(cmds4) == len(confs4))

    def testDeltaflash(self):
        # test find vpl file
        utilsHelper.debug.debug('delta flash')
        self.product.imei = '004402478661956'
        flasher = self.utilsHelper.getFlasher(self.product, 'delta')
        vplfile = self.utilsHelper.findFirstFile('*.vpl')
        self.assertTrue('RM1057_059W0Q7_0.1426.0.0_006.vpl' in vplfile)
        self.assertEqual(flasher.setTestMode,
                         'DeltaConsoleFlasher setMode -e %s -m Test \
-i %s' % (flasher.deviceType, self.product.imei))
        # flasher.flash()
        
    def testDeltaSetmode(self):
        self.product.imei = '0044024786619560'
        self.product.productname = 'athena'
        flasher = self.utilsHelper.getFlasher(self.product, 'delta')
        flasher.makeFlashCmd('./*.vpl')

    def testEnviron(self):
        self.product.imei = '0044024786619560'
        self.product.productName = 'athena'
        flasher = self.utilsHelper.getFlasher(self.product, 'delta')
        imeis = flasher.getImeis('config.xml')
        imeis = [imei[0: -1] for imei in imeis if len(imei) == 16]
        # self.assertIn('004402478662905', imeis)

    def testSwithclan(self):
        self.product.imei = '0044024786619560'
        self.product.productName = 'athena'
        self.product.sn = 'ff0acb'
        # self.utilsHelper.switchLanguage(self.product, 'en', 'US')
        # self.utilsHelper.rebootTarget(self.product)
        # self.assertTrue(self.utilsHelper.checkLanguage(self.product, 'en'))

    def testRaiseException(self):
        try:
            self.utilsHelper.raiseException('testRaiseException')
        except Exception:
            pass

        with open('./results/error.log', 'r') as f:
            self.assertTrue('testRaiseException' in f.readline())

    def testCtsMediaCopy(self):
        from cts.run import CTS

        cts = CTS(products=[self.product], filename=None, items=['test'])
        cts.source_conf = '../cts/media_win.xml'
        confs = cts.getMediaConf()
        self.assertTrue(confs)
        import xml.etree.cElementTree as ET
        copyPropertys = []
        doc = ET.parse('../cts/media_win.xml')
        root = doc.getroot()
        src_root = root.attrib['src_root']
        dest_root = root.attrib['dest_root']
        for item in root.findall('item'):
            src = os.path.join(src_root, item.attrib['src'])
            dest = os.path.join(dest_root, item.attrib['dest'])
            copyPropertys.append((src, dest))

        self.assertEqual(confs, copyPropertys)

    def test_cts_mediaCopycmds(self):
        from cts.run import CTS

        cts = CTS(products=[self.product], filename=None, items=['test'])
        confs = cts.getMediaConf()
        cmds = []
        for src, dest in confs:
            cmd = 'adb -s %s push %s %s' % (self.product.sn, src, dest)
            cmds.append(cmd)

        cmd2s = cts.buildCopyMediaCmds(self.product.sn, confs)
        self.assertEqual(cmds, cmd2s)

    def test_cts_mediaConf(self):
        from cts.run import CTS
        cts = CTS(products=[self.product], filename=None, items=['test'])
        if utilsHelper.isWindows:
            self.assertEqual('media_win.xml', cts.source_conf)
        else:
            self.assertEqual('media_lin.xml', cts.source_conf)

    def test_cts_getrunenvirnmentcmds(self):
        print 'test_cts_getrunenvirnmentcmds'
        from cts.run import CTS
        cts = CTS(products=[self.product], filename=None, items=['test'])
        cts.runconf = '../cts/runconf.xml'
        confs = cts.getRunEnvirnmentConf()
        cmds = cts.getRunEnvirnmentCmds(self.product, confs)
        self.assertIsNotNone(cmds)

    def test_device_info_file(self):
        from execute import showDeviceInfo
        showDeviceInfo(self.product)
        self.assertTrue(os.path.exists('./results/deviceinfo.log'))

    def test_cmd_ext_flash_args_1(self):
        print 'test_cmd_ext_flash_args'
        cmdline = 'custom=1.custom.img,2.custom.img'

        ext_files = utilsHelper.commandLine.buildExtflashArgs(cmdline)
        result = [('custom', ['1.custom.img', '2.custom.img'])]
        self.assertEqual(result, ext_files)

    def test_cmd_ext_flash_args_parse(self):
        cmdline = 'custom=c1.img,c2.img'

        result = [{'custom': 'c1.img'}, {'custom': 'c2.img'}]
        ret = utilsHelper.commandLine.getFlashArgs(cmdline)
        self.assertEqual(result, ret)
        ret = utilsHelper.commandLine.getFlashArgs(cmdline)
        self.assertEqual(ret, utilsHelper.getFlashArgs(cmdline))
        self.assertEqual(result, ret)

    def test_cmd_ext_flash_args_2(self):
        cmdline = 'custom=1.custom.img,2.custom.img;boot=b1.img,b2.img'

        ext_files = utilsHelper.commandLine.buildExtflashArgs(cmdline)
        result = [('custom', ['1.custom.img', '2.custom.img']),
                  ('boot', ['b1.img', 'b2.img'])]
        self.assertEqual(result, ext_files)

    def test_ping_device(self):
        print 'ping device'
        self.product.imei = '004402478661956'
        # self.assertTrue(utilsHelper.pingDevice(self.product))

    def test_active_usb(self):
        self.product.imei = '004402478661956'
        # self.assertTrue(utilsHelper.activeUsb(self.product))

    def test_json_file(self):
        print 'test_json_file'
        import json
        f = open('json.json')
        decodeJson = json.loads(f.read())
        param = decodeJson['json'][0]['parameters']
        args = ' --resultd "test_result"'
        decodeJson['json'][0]['parameters'] = param.join(args)

    def test_getdevices_from_devicesjson(self):
        from utils.jsondata import DeviceParser
        parser = DeviceParser(utilsHelper, 'devices.json')
        utilsHelper.debug.level = 4
        devices = parser.getDevices()
        self.assertIsNotNone(devices[0].__getattribute__('sn'))


FLASH = True
UT.main()








