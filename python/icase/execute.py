# coding -*- utf-8 _8-
from utils.utils import utilsHelper
from utils.utils import JunitParser, IcaseLogger
import importlib
import json
import os


def getModule(modulename):
    utilsHelper.debug('%s.run' % modulename)
    run = importlib.import_module('%s.run' % modulename)
    return run


def getJsonInstances(indexfile):
    f = open(indexfile)
    files = []
    for line in f.readlines():
        line = line.replace('\n', '')
        utilsHelper.debug(line)
        files.append(line.replace('\n', ''))
    f.close()

    jsonList = []
    for file in files:
        if len(file) < 4:
            utilsHelper.debug('index file has empty line')
            continue
        utilsHelper.debug('load %s' % file)
        f = open(file, 'r')
        jsonObj = json.loads(f.read())
        jsonList.append((jsonObj, file))
        f.close()
    return jsonList


logger = IcaseLogger('./results/flash.log')
utilsHelper.setLogger(logger)


def showDeviceInfo(device):
    with open('./results/deviceinfo.log', 'w') as f:
        f.write('%s %s' % (device.productname, device.sn))
    utilsHelper.debug.info('%s %s' % (device.productname, device.sn))


def flashPhone(product, flashTool='fastboot', parts_files=None):
    # custom=*custom.img;boot=boot.img
    if not parts_files:
        parts_files = {}
    else:
        utilsHelper.debug.info(str(parts_files))
    flasher = utilsHelper.getFlasher(product, flashTool=flashTool)
    flasher.setFlashFiles(parts_files)
    return flasher.flash(steptimeout=300)


def main():
    utilsHelper.debug.info('Enter execute module v2.0')
    cmdparams, vars = utilsHelper.parseCmdLine()
    if cmdparams.result:
        utilsHelper.resultName = cmdparams.result
        utilsHelper.debug('result name: %s' % utilsHelper.resultName)
    else:
        utilsHelper.resultName = 'result.zip'

    if not os.path.exists('index'):
        utilsHelper.debug("error can not found index file")
        utilsHelper.raiseException('index file not found')
        return

    # parse devices.json
    if os.path.exists('devices.json'):
        products = utilsHelper.getDevices('devices.json')
        # ParseProductJson('devices.json').parse()
    else:
        utilsHelper.debug("Can not found devices.json file")
        utilsHelper.raiseException('devices json file not found')
        return

    # check the right products
    if not products:
        utilsHelper.raiseException('products is empty')
        return

    for product in products:
        showDeviceInfo(product)
        if cmdparams.flash:
            flash_files = {}
            if cmdparams.flash_args:
                utilsHelper.debug.info(cmdparams.flash_args)
                args = cmdparams.flash_args
                flash_files = utilsHelper.getFlashArgs(args)

            flash_file = {}
            if flash_files:
                flash_file = flash_files[0]

            if not flashPhone(product, cmdparams.flash, flash_file):
                utilsHelper.raiseException('flash phone failed')
                return

            utilsHelper.disableFirstTimeUse(product)
            utilsHelper.switchLanguage(product, 'en', 'US')
        # end flash

        # initial phone status
        utilsHelper.setSreenTimeout(product)
        utilsHelper.simCardInit(product)
        utilsHelper.clearsdcard1(product)
        utilsHelper.rebootTarget(product)
        # check the language is except
        if cmdparams.flash:
            if not utilsHelper.checkLanguage(product, 'en'):
                utilsHelper.debug.info('retry to switch language')
                utilsHelper.switchLanguage(product, 'en', 'US')
                utilsHelper.rebootTarget(product)
                if not utilsHelper.checkLanguage(product, 'en'):
                    utilsHelper.raiseException('switch language failed')

        utilsHelper.installTesthelper(product)
        utilsHelper.setSimOnline(product)

        #  run test case
        jsonlist = getJsonInstances('index')
        hasFailed = False
        for jsonObj, file in jsonlist:
            utilsHelper.debug('starting %s' % jsonObj['type'])
            currentworkspace = os.path.abspath(os.getcwd())
            testType = jsonObj['type']
            moduleLauncher = getModule(testType)
            moduleLauncher.Start(products, file, decodeJson=jsonObj)
            os.chdir(currentworkspace)
            if utilsHelper.getLastError() != 0:
                hasFailed = True

    # end for products

    if not os.path.exists('./results/njunit.xml'):
        jparser = JunitParser()
        jparser.parse('./results/njunit.xml')
        utilsHelper.addDirArchive(utilsHelper.resultName, './results')
    if hasFailed:
        utilsHelper.raiseException('Execute failed')


if __name__ == '__main__':
    main()
