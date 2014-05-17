#coding -*- utf-8 _8-
from utils.utils import Parse,utilsHelper
import importlib ,json,os,platform

def getModule(modulename):
    print '%s.run'%modulename
    run =importlib.import_module('%s.run'%modulename) 
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
            print '%s = %s'%(name, value)

class ParseProductJson(Parse):

    def __init__(self, data):
        self.data = data
        self.products =[]

    def parse(self):
        assert self.data is not None
        f = open(self.data)
        try: 
            decodeJson = json.loads(f.read())
            for jsonitem in decodeJson:
                product = Product()
                product.role=jsonitem['role']
                product.detailedConnectionId=jsonitem['id']
                product.sn = jsonitem['attributes']['sn']
                product.imei=jsonitem['attributes']['imei']
                product.productName = jsonitem['attributes']['productname']
                product.connectionId = jsonitem['status']['id']
                #marble property item
                settingsItems = ['BluetoothName','Connection','SIM1PhoneNumber',
                                'SIM1Pin2Code','SIM1PinCode','SIM1Puk1Code','SIM1Puk2Code',
                                'SIM1ServiceNumber','SIM1VoiceMailNumber','SIM2PhoneNumber',
                                'SIM2Pin2Code','SIM2PinCode','SIM2Puk1Code','SIM2Puk2Code',
                                'SIM2ServiceNumber','SIM2VoiceMailNumber','SecurityCode',
                                'TraceConnection','WLANName','WLANName2','WLANPassword',
                                'WLANPassword2','VoIPAccount','VoIPPassword']

                for subitem in settingsItems:
                    if jsonitem['attributes'].has_key(subitem):
                        print 'set setting item %s var: <%s>'%(subitem,jsonitem['attributes'][subitem])
                        product.__setattr__(subitem,jsonitem['attributes'][subitem])
                self.products.append(product)
        finally:
            f.close()
        return self.products
        
def getJsonInstances(indexfile):
    f = open(indexfile)
    files = []
    for line in f.readlines():
        files.append(line.replace('\n',''))
    f.close()

    jsonList =[]
    for file in files:
        f = open(file,'r')
        jsonObj = json.loads(f.read())
        jsonList.append((jsonObj,file))
        f.close()
    return jsonList
def flashPhone(productSN):
    import time,shutil
    #copy flash bat from flash folder
    print 'flash_device %s' % productSN
    if not os.path.exists('results'):
        os.makedirs('results')
    status = False
    if platform.system() == 'Windows':
        shutil.copyfile('flash/windows_flash_device.bat','./windows_flash_device.bat')
        retVal =  os.system('windows_flash_device.bat %s > results/flash.log' % productSN)
        print 'flash return %s'%retVal
        if retVal==0:
            print 'windows_flash_device.bat %s finished'%productSN
            print 'waiting phone restarting'
            time.sleep(100)
            status = True
        else:
            status = False
    else:
        shutil.copyfile('flash/linux_flash_device.sh','./linux_flash_device.sh')
        retVal = os.system('linux_flash_device.sh %s > results/flash.log' % productSN)
        print 'flash return %s'%retVal
        if retVal==0:
            print 'linux_flash_device.sh %s finished'%productSN
            print 'waiting phone restarting'
            status = True
        else:
            status = False
    utilsHelper.addArchive('result.zip', 'results/flash.log')
    if not status:
        print 'flash failed see results/flash.log for more details please'
    else:
        time.sleep(100)
    
    return status
    
def main():
    print 'Enter execute module'
    cmdparams,vars = utilsHelper.parseCmdLine()
    print cmdparams
    if not os.path.exists('index'):
        print "error can not found index file"
        return 
            
    #command starter
    if cmdparams.testtype:
        print 'starting %s' % cmdparams.testtype
        products = ParseProductJson(cmdparams.product).parse()
        if cmdparams.flash:
            for product in products:
                flashPhone(product.sn)
                utilsHelper.installTesthelper(product)
        currentworkspace = os.path.abspath(os.getcwd())
        moduleLauncher = getModule(cmdparams.testtype)
        items = moduleLauncher.CreateItem(cmdparams)
        moduleLauncher.Start(products,cmdparams.testtype+'.json',items = items)
        os.chdir(currentworkspace)
    else:
        print 'starting parse the index file'
        #parse index
        if os.path.exists('devices.json'):
            products = ParseProductJson('devices.json').parse()
        else:
            print "Can not found devices.json file"
            return
        for product in products:
            print 'flash %s'% product.sn
            if cmdparams.flash:
                flashPhone(product.sn)
            utilsHelper.installTesthelper(product)

        jsonlist = getJsonInstances('index')
        for jsonObj,file in jsonlist:
            print 'starting %s' % jsonObj['type']
            currentworkspace = os.path.abspath(os.getcwd())
            testType = jsonObj['type']
            moduleLauncher = getModule(testType)
            moduleLauncher.Start(products,file, decodeJson=jsonObj)
            os.chdir(currentworkspace)
if __name__ == '__main__': 
    main()
    
