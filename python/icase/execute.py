#coding -*- utf-8 _8-
#from marble.run import Marble

from utils.utils import UtilsHelper,Parse

import importlib ,json,os,platform

def getModule(modulename):
    print '%s.run'%modulename
    run =importlib.import_module('%s.run'%modulename) 
    return run
#marble = run.Start(None,None)

class Product(object): 
    def __init__(self):
        self.sn = None
        self.imei = None
        self.role = None
        self.connectionId = None
        self.detailedConnectionId = None
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
                product.connectionId = jsonitem['status']['id']
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
    if platform.system() == 'Windows' and os.path.exists('Ara_flash_device.bat'):
        os.system('Ara_flash_device.bat %s'%productSN)
    elif os.path.exists('Ara_flash_device.sh'):
        os.system('Ara_flash_device.sh %s'%productSN)
    else:
        print 'flash error %s'%productSN
        
def main():
    utilHelper = UtilsHelper()
    
    cmdparams,vars = utilHelper.parseCmdLine()
    
    #command starter
    if cmdparams.testtype:
        products = ParseProductJson(cmdparams.product).parse()
        for product in products:
            flashPhone(product.sn)
        currentworkspace = os.path.abspath(os.getcwd())
        moduleLauncher = getModule(cmdparams.testtype)
        items = moduleLauncher.CreateItem(cmdparams)
        moduleLauncher.Start(products,cmdparams.testtype+'.json',items = items)
        os.chdir(currentworkspace)
    else:    
        #parse index 
        products = ParseProductJson('devices.json').parse()
        for product in products:
            flashPhone(product.sn)
        jsonlist = getJsonInstances('index')
        for jsonObj,file in jsonlist:
            currentworkspace = os.path.abspath(os.getcwd())
            testType = jsonObj['type']
            moduleLauncher = getModule(testType)
            moduleLauncher.Start(products,file, decodeJson=jsonObj)
            os.chdir(currentworkspace)
if __name__ == '__main__': 
    main()
    