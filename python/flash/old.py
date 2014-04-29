#coding -*- utf-8 _8-

import shutil，os, sys, json, time, subprocess, zipfile
from utils import *

    def __init__(self, workspace = '.'): 
        self.workspace = workspace 

    def run(self, command, logfilename): 
        exitcode = 0 
        try: 
            tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 
            toolOutputs = tool.stdout
            logger = Writer(logfilename, sys.stdout)
            sys.stdout = logger
            while 1: 
                outputFromTool = toolOutputs.readline() 
                time.sleep(1.0 / 1000.0) 
                if not outputFromTool: 
                    break 

                print 'Tool: ' + outputFromTool 

            exitcode = tool.wait()
            sys.stdout = sys.__stdout__
            logger.store(self.workspace)
            print 'Tool execution finished' 
        except OSError, e:
            sys.stdout = sys.__stdout__ 
            print 'An error occured during execution: ', e 

        return exitcode 
    
    def runMonkey(self, toolArguments, logfilename): 
        '''
        run the monkey test use adb
        '''
        # Prepare command 
        command='adb' 
        command += toolArguments 
        print command
        self.run(command, logfilename)
    def runInstrument(self, toolArguments, logfilename):
        command = 'adb'
        command += toolArguments
        print command
        self.run(command, logfilename)

    def runMarble(self, toolArguments, logfilename):
        '''
        run the marble use ipy
        '''
        command = 'ipy'
        command += toolArguments
        print command
        self.run(command, logfilena
class Product: 
    def __init__(self):
        self.sn = None
        self.imei = None
        self.role = None
        self.connectionId = None
        self.detailedConnectionId = None
        
    def showDetails(self): 
        print ' --- PRODUCT --- '
        print 'SN:                   %s'% str(self.sn) 
        print 'IMEI:                 %s'% str(self.imei) 
        print 'Role:                 %s'% str(self.role)
        print 'ConnectionId:         %s'% str(self.connectionId)
        print 'DetailedConnectionId: %s'% str(self.detailedConnectionId)
        print ' --------------- ' 

#############################################################
class Parse(object):
    
    def parse(self):
        return None
    def getJsonName(self, jsonfilename):
        return jsonfilename[0:-5]
    
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

class MonkeyItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)
        
class MarbleItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)
        self.marbleTool = None
        self.testset = None

class InstrumentItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)
        self.apkName = None
        self.package = None
        self.testapk = None
        self.runner = None

def DisplayItems(items):
    for item in items:
        item.displayAttributes()
        
def DisplayApkItems(apkitems):
    for item in apkitems:
        item.displayAttributes()
        

class MonkeyJsonParser(Parse):
    def __init__(self, filename =None):
        self.filename = filename
    def parseObj(self, decodeJson):
        item = MonkeyItem()
        item.itemType = decodeJson['type']
        item.itemName = self.getJsonName(self.filename)
        item.parameters = decodeJson[item.itemName][0]['parameters']

class InstrumentJsonParser(Parse):
    def __init__(self, filename = None):
        self.filename = filename
    
    def parseObj(self,decodeJson):
        apkItem = InstrumentItem()
        apkItem.itemtype = decodeJson['type']
        apkItem.itemName = self.getJsonName(self.filename)
        apkItem.apkName =decodeJson[apkItem.itemName][0]['apk']
        apkItem.package = decodeJson[apkItem.itemName][0]['package']
        apkItem.testapk = decodeJson[apkItem.itemName][0]['testapk']
        apkItem.testpackage = decodeJson[apkItem.itemName][0]['testpackage']
        apkItem.runner = decodeJson[apkItem.itemName][0]['runner']
        apkItem.parameters = decodeJson[apkItem.itemName][0]['parameters']
        return [apkItem]
    
    def parse(self,files):
        if isinstance(files,list):
            apkItems =[]
            for file in files:
                print 'parse file %s '%file
                apkItem = InstrumentItem()
                f = open(file)
                decodeJson = json.loads(f.read())
                f.close()
                apkItem.itemtype = decodeJson['type']
                apkItem.itemName = self.getJsonName(file)
                apkItem.apkName =decodeJson[apkItem.itemName][0]['apk']
                apkItem.package = decodeJson[apkItem.itemName][0]['package']
                apkItem.testapk = decodeJson[apkItem.itemName][0]['testapk']
                apkItem.testpackage = decodeJson[apkItem.itemName][0]['testpackage']
                apkItem.runner = decodeJson[apkItem.itemName][0]['runner']
                apkItem.parameters = decodeJson[apkItem.itemName][0]['parameters']
                apkItems.append(apkItem)
                
            return apkItems

class ExecuteHelper():
    def __init__(self):
        
        self.uninstalllist = ['com.android.notepad', 'com.notepadblackboxtest']
        self.installlist = ['NotePad.apk', 'NotePadBlackBoxTest.apk']
        self.products = []

    def parseProductFile(self,jsonfile):

        if jsonfile:
            self.products = ParseProductJson(jsonfile).parse()
            print 'init products info %s'%jsonfile
        else:
            #using default data
            if os.path.exists('devices.json'):
                self.products = ParseProductJson('devices.json').parse()
                print 'init products info %s'%jsonfile
        return self.products

    def getProductsSn(self):
        return [product.sn for product in self.products]
    
    def getProducts(self):
        return self.products
    
    def parseCmdLine(self):
                
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-p', '--product', dest = 'product', help = 'contains product information')
        parser.add_option('-f', '--flash', dest = 'flashtool',help = 'flash tool name and path')
        parser.add_option('-t', '--testset', dest ='testset', help='test case configure contains test case')
        parser.add_option('-i',"--instrument",action='store_true' , help = 'instrument test')
        parser.add_option('-m', '--marble', action ='store_true',dest = 'marble', help ='marble test')
        parser.add_option('-A', '--marbletool',dest = 'marbletool',help ='marble tools name eg: ../marble.py')
        parser.add_option('-M', '--Monkey', dest = 'Monkey', help = 'Monkey test')
        parser.add_option('-l', '--logfile', dest = 'logfile', help = 'log file save the result')
        parser.add_option('-T', '--testmode', dest ='testmode',action = 'store_false', help = 'for test mode for development')

        return parser.parse_args()[0]

executeHelper = ExecuteHelper()
class Logger:
    def __init__(self,logfile):

        self.filename = logfile
        self.logfile = open(logfile,'w')

    def append(self,log):
        self.logfile.write(log)
        self.logfile.flush()

    def store(self, workspace,compressFileName): 
        print 'compressing test results to %s' % os.path.join(workspace,compressFileName)
        zf = zipfile.ZipFile(os.path.join(workspace,compressFileName), 'a') 
        try: 
            print 'adding %s' % self.filename
            zf.write(self.filename) 
        finally: 
            zf.close()
            self.logfile.close()

class TestTool(object):
    def __init__(self):
        pass
    def run(self):
        pass
    def generatorLogfileName(self, testset):

        tmpstr = testset.replace('\\','/')
        testsetname = tmpstr.split('/')[-1]
        if len(testset) > 2:
            logfilename = "%s_%s%s"%(self.name,testsetname,'.log')
        return logfilename

class Monkey(TestTool):
    def __init__(self, products, items):
        self.resultdirs = './results'
        self.logName = 'Monkey.log'
        self.name = 'Monkey'
        self.products = products
        self.items = items
        self.compressName = 'result.zip'
    def getCommand(self, toolArguments):
        cmd = 'adb %s'%toolArguments
        return cmd
    
    def _run(self,logger, toolArguments):
        command = self.getCommand(toolArguments)
        exitcode = 0
        print 'run %s'%command
        try: 
            tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            toolOutputs = tool.stdout
            while 1: 
                outputFromTool = toolOutputs.readline() 
                time.sleep(1.0 / 1000.0) 
                if not outputFromTool: 
                    break 
                print 'Tool: ' + outputFromTool 
                logger.append(outputFromTool)
            exitcode = tool.wait()
            print 'Tool execution finished' 
        except OSError, e:
            print 'An error occured during execution: ', e 
        return exitcode
    
    def run(self):
        for product in self.products:
            for item in self.items:
                logger = self.prepareLogger(os.path.join(self.resultdirs,item.itemName))
                toolArguments = ' -s '+product.sn +' shell monkey '+ item.parameters
                self._run(logger, toolArguments)
                logger.store(self.workspace, self.compressName)

class Instrument(TestTool):
    def __init__(self, products,apkItems):
        self.resultdirs = './results'
        self.logName = 'result.log'
        self.workspace = '.'
        self.name = 'Instrument'
        self.products = products
        self.apkItems = apkItems
        self.compressName = 'result.zip'
        #inclue apk info and parameters
    def setLogName(self, logName):
        self.logName = logName
        
    def prepareLogger(self,resultdirs):
        if not os.path.exists(resultdirs):
            os.makedirs(resultdirs)
        print 'log file %s'%os.path.join(resultdirs,self.logName)
        return Logger(os.path.join(resultdirs,self.logName))
    
    def getCommand(self,toolArguments):
        command = 'adb %s' % toolArguments
        return command

    def _run(self,logger, toolArguments):

        command = self.getCommand(toolArguments)
        exitcode = 0
        print 'run %s'%command
        try: 
            tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            toolOutputs = tool.stdout
            while 1: 
                outputFromTool = toolOutputs.readline() 
                time.sleep(1.0 / 1000.0) 
                if not outputFromTool: 
                    break 
                print 'Tool: ' + outputFromTool 
                logger.append(outputFromTool)
            exitcode = tool.wait()
            print 'Tool execution finished' 
        except OSError, e:
            print 'An error occured during execution: ', e 
        return exitcode 
    # workspace 
    # ----results
    # --------NotePad
    # ------------result.log            (Could be any name that ends with '.log')
    def run(self):
        for product in self.products:
            for apkItem in self.apkItems:
                self.setLogName(self.generatorLogfileName(apkItem.testpackage))
                logger = self.prepareLogger(os.path.join(self.resultdirs,apkItem.apkName[0:-4]))

                instrumentCmd = ' -s ' + product.sn + ' uninstall ' + apkItem.package
                self._run(logger, instrumentCmd)

                instrumentCmd = ' -s ' + product.sn + ' uninstall ' + apkItem.testpackage
                self._run(logger, instrumentCmd)

                instrumentCmd = ' -s %s install %s'%(product.sn ,apkItem.apkName)
                self._run(logger, instrumentCmd)

                instrumentCmd = ' -s %s install %s'%(product.sn ,apkItem.testapk)
                self._run(logger,instrumentCmd)

                instrumentCmd = ' -s %s shell am instrument -r -w %s/%s %s'%(product.sn, apkItem.testpackage, apkItem.runner, apkItem.parameters)
                self._run(logger,instrumentCmd)

                logger.store(self.workspace,self.compressName)

class Marble(TestTool):
    def __init__(self,commandTool, products, items):
        self.testItems = items
        self.name = "Marble"
        self.products = products
        self.commandTool = commandTool

    def run(self):

        assert self.testItems
        marbleTool = self.testItems[0].marbleTool
        
        if os.path.exists(marbleTool) and not os.path.exists('marble'):
            shutil.copytree(marbleTool,'marble')
            print 'copy %s to %s' % (marbleTool,os.path.abspath('./marble'))

        print 'change work dir to %s'%os.path.abspath('./marble/framework')
        os.chdir('./marble/framework')
        for product in self.products:
            for item in self.testItems:
                marbleCommand = " marble.py --connection %s --test_set %s %s"% (product.sn, item.testset, item.parameters)        
                self.commandTool.runMarble(marbleCommand, self.generatorLogfileName(item.testset))
                
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
        
def main(): 
    # Product list
    #step 1: parse the command line for products
    cmdparams = executeHelper.parseCmdLine()
    executeHelper.parseProductFile('devices.json')
    products = executeHelper.getProducts()
    #display the products
    DisplayProducts(products)
    #step 2 flash
    flashtool = cmdparams.ensure_value('flashtool',None)
    flashCmd = None
    if flashtool:
        flashCmd = flashtool
        
    if flashCmd and os.path.exists(flashCmd):
        os.system(flashCmd)
    else:
        print 'no flash cmd have been found'
 #       return

    #step3 start test case
    tool = CommandTool(os.path.abspath('.'))
    #read the index file
    jsonlist = getJsonInstances('index')
    for jsonObj,file in jsonlist:
        testType = jsonObj['type']
        print file , testType
        if  testType in 'robotium':
            print 'run robotium test'
        elif testType in 'instrument':
            print 'starting instrument test...'
            parseinstrument = InstrumentJsonParser(file)
            items = parseinstrument.parseObj(jsonObj)
            DisplayApkItems(items)
            instrument = Instrument(products, items)
            instrument.run()
        elif testType in 'marble':
            print 'starting marble test...'
            marbleParser = MarbleJsonParser(file)
            items = marbleParser.parseObj(jsonObj)
            DisplayItems(items)
            marble = Marble(tool,products,items)
            marble.run()
        elif testType in 'Monkey':
            pass

    print 'finished'
    return
    marble = cmdparams.ensure_value("marble", None)
    if marble:
        marbletool = cmdparams.ensure_value('marbletool',None)
        marble = Marble(tool, marbletool, products)
        testset = cmdparams.ensure_value('testset',None)
        marble.run(testset)
        
    #instrument test
    instrument = cmdparams.ensure_value('instrument', None)
    if instrument:
        print 'starting instrument testing ...'
        #get the apktestitems from config file
        f = open('index')
        files = []
        for line in f.readlines():
            files.append(line.replace('\n',''))
        f.close()

        parseinstrument = InstrumentJsonParser()
        items = parseinstrument.parse(files)
        DisplayApkItems(items)

        instrument = Instrument(products, items)
        instrument.run()
                
    print 'finished'
if __name__ == '__main__': 
    main_()
    

