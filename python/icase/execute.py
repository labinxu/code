# coding -*- utf-8 _8-
from utils.utils import Parse, utilsHelper, debug, JunitParser, Flasher
import importlib
import json
import os


def getModule(modulename):
    debug.debug('%s.run' % modulename)
    run = importlib.import_module('%s.run' % modulename)
    return run


class Product(object):
    def __init__(self):
        self.sn = None
        self.imei = None
        self.role = None
        self.connectionId = None
        self.detailedConnectionId = None
        self.productName = None

    def displayAttributes(self):
        for name, value in vars(self).items():
            debug.debug('%s = %s' % (name, value))


class ParseProductJson(Parse):

    def __init__(self, data):
        self.data = data
        self.products = []

    def parse(self):
        assert self.data is not None
        f = open(self.data)
        try:
            decodeJson = json.loads(f.read())
            for jsonitem in decodeJson:
                product = Product()
                product.role = jsonitem['role']
                product.detailedConnectionId = jsonitem['id']
                product.sn = jsonitem['attributes']['sn']
                product.imei = jsonitem['attributes']['imei']
                product.productName = jsonitem['attributes']['productname']
                product.connectionId = jsonitem['status']['id']
                product.simcount = 1

                if 'simcount' in jsonitem['attributes'].keys():
                    product.simcount = int(jsonitem['attributes']['simcount'])
                debug.debug('simcount = %d' % product.simcount)
                # marble property item
                settingsItems = ['BluetoothName',
                                 'Connection', 'SIM1PhoneNumber',
                                 'SIM1Pin2Code', 'SIM1PinCode',
                                 'SIM1Puk1Code', 'SIM1Puk2Code',
                                 'SIM1ServiceNumber',
                                 'SIM1VoiceMailNumber',
                                 'SIM2PhoneNumber',
                                 'SIM2Pin2Code',
                                 'SIM2PinCode',
                                 'SIM2Puk1Code',
                                 'SIM2Puk2Code',
                                 'SIM2ServiceNumber',
                                 'SIM2VoiceMailNumber',
                                 'SecurityCode',
                                 'TraceConnection',
                                 'WLANName',
                                 'WLANName2', 'WLANPassword',
                                 'WLANPassword2', 'VoIPAccount',
                                 'VoIPPassword']

                for subitem in settingsItems:
                    if subitem in jsonitem['attributes'].keys():
                        debug.debug('set setting item %s var: <%s>' %
                                    (subitem, jsonitem['attributes'][subitem]))
                        product.__setattr__(subitem,
                                            jsonitem['attributes'][subitem])
                # add security code for 3.0
                product.__setattr__('SecurityCode', '201449')
                self.products.append(product)
        except KeyError, e:
            debug.error('Can not found %s Please check the json file' % e)
            self.products = None
        finally:
            f.close()
        return self.products


def getJsonInstances(indexfile):
    f = open(indexfile)
    files = []
    for line in f.readlines():
        line = line.replace('\n', '')
        debug.debug(line)
        files.append(line.replace('\n', ''))
    f.close()

    jsonList = []
    for file in files:
        if len(file) < 4:
            debug.debug('file error'+file)
            continue
        debug.debug('load %s' % file)
        f = open(file, 'r')
        jsonObj = json.loads(f.read())
        jsonList.append((jsonObj, file))
        f.close()
    return jsonList


def flashPhone2(product):
    
    flasher = Flasher(utilsHelper, productSN=product.sn)
    flasher.flash()
    if utilsHelper.getLastError() != 0:
        return False
    else:
        return True


def main():
    debug.debug('Enter execute module')
    cmdparams, vars = utilsHelper.parseCmdLine()
    debug.debug(cmdparams)
    if cmdparams.result:
        utilsHelper.resultName = cmdparams.result
        debug.debug('result name: %s' % utilsHelper.resultName)
    else:
        utilsHelper.resultName = 'result.zip'

    if not os.path.exists('index'):
        debug.debug("error can not found index file")
        utilsHelper.raiseException('index file not found')
        return

    # command starter
    if cmdparams.testtype:
        debug.debug('starting %s' % cmdparams.testtype)
        products = ParseProductJson(cmdparams.product).parse()
        if cmdparams.flash:
            for product in products:
                if not flashPhone2(product):
                    utilsHelper.raiseException('flash phone failed')
                    return
                utilsHelper.installTesthelper(product)
        currentworkspace = os.path.abspath(os.getcwd())
        moduleLauncher = getModule(cmdparams.testtype)
        items = moduleLauncher.CreateItem(cmdparams)
        moduleLauncher.Start(products, cmdparams.testtype+'.json', items=items)
        os.chdir(currentworkspace)
    else:
        debug.debug('starting parse the index file')
        # parse index
        if os.path.exists('devices.json'):
            products = ParseProductJson('devices.json').parse()
        else:
            debug.debug("Can not found devices.json file")
            utilsHelper.raiseException('devices json file not found')
            return
        # check the right products
        if not products:
            utilsHelper.raiseException('products is empty')
            return

        for product in products:
            if cmdparams.flash:
                if not flashPhone2(product):
                    utilsHelper.raiseException('flash phone failed')
                    return
            utilsHelper.installTesthelper(product)

        jsonlist = getJsonInstances('index')
        hasFailed = False
        for jsonObj, file in jsonlist:
            debug.debug('starting %s' % jsonObj['type'])
            currentworkspace = os.path.abspath(os.getcwd())
            testType = jsonObj['type']
            moduleLauncher = getModule(testType)
            moduleLauncher.Start(products, file, decodeJson=jsonObj)
            os.chdir(currentworkspace)
            if utilsHelper.getLastError() != 0:
                hasFailed = True

        if not os.path.exists('./results/njunit.xml'):
            jparser = JunitParser()
            jparser.parse('./results/njunit.xml')
            utilsHelper.addDirArchive(utilsHelper.resultName, './results')

        if hasFailed:
            utilsHelper.raiseException('Execute failed')
if __name__ == '__main__':
    main()
