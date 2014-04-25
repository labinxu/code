#coding -*- utf-8 _8-

import os, sys, json, time, subprocess, zipfile
import shutil
class writer: 
    def __init__(self, logfile, stdout): 
        self.stdout = stdout 
        self.logfile = logfile 
        self.log = file(logfile, 'w') 
    def write(self, text): 
        self.stdout.write(text) 
        self.log.write(text) 
        self.stdout.flush() 
        self.log.flush() 
    def store(self, workspace): 
        print 'compressing test results to ' + workspace + '/results.zip' 
        zf = zipfile.ZipFile(workspace + '/results.zip', 'a') 
        try: 
            print 'adding ' + self.logfile 
            zf.write(self.logfile) 
        finally: 
            zf.close()

class commandTool: 
    def __init__(self, workspace = '.'): 
        self.workspace = workspace 

    def run(self, command, logfilename): 
        exitcode = 0 
        try: 
            tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 
            toolOutputs = tool.stdout
            logger = writer(logfilename, sys.stdout)
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
        self.run(command, logfilename)
    
class ADBManger():
    
    def __init__(self):
        self.adbProcess = None

    def getPopenObje(self):
        return self.adbProcess
    
    def createProcess(self, args):
        '''
        Create an adb process with args
        example adb logcat
        '''
        self.adbProcess = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        
    def endProcess(self):
        self.adbProcess.kill()
        
def DisplayProducts(products):
    for product in products:
        product.showDetails()

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
                product.sn = jsonitem['attributes']['sn']
                product.imei=jsonitem['attributes']['imei']
                product.role=jsonitem['role']
                product.detailedConnectionId=jsonitem['id']
                decodeStatus=json.loads(jsonitem['status'])
                product.connectionId=decodeStatus['id']

                self.products.append(product)
        finally:
            f.close()
        return self.products
class ApkTestItem(object):
    def __init__(self):
        self.itemtype = None
        self.itemName = None
        self.apkName = None
        self.package = None
        self.testapk = None
        self.parameters = None
        self.runner = None
    def displayAttributes(self):
        for name, value in vars(self).items():
            print '%s = %s'%(name, value)
def DisplayApkItems(apkitems):
    for item in apkitems:
        item.displayAttributes()
    
class ParseInstrumentJson(Parse):
    def __init__(self, data):
        self.data = data
    def getApkTestName(self, jsonfilename):
        assert jsonfilename is not None

        return jsonfilename[0:-5]
        
    def parse(self,files):
        if isinstance(files,list):
            apkItems =[]
            for file in files:
                apkItem = ApkTestItem()
                f = open(file)
                decodeJson = json.loads(f.read())
                apkItem.itemtype = decodeJson['type']
                apkItem.itemName = self.getApkTestName(file)
                apkItem.apkName =decodeJson[apkItem.itemName][0]['apk']
                apkItem.package = decodeJson[apkItem.itemName][0]['package']
                apkItem.testapk = decodeJson[apkItem.itemName][0]['testapk']
                apkItem.testpackage = decodeJson[apkItem.itemName][0]['testpackage']
                apkItem.runner = decodeJson[apkItem.itemName][0]['runner']
                apkItem.parameters = decodeJson[apkItem.itemName][0]['parameters']
                apkItems.append(apkItem)
                f.close()
            return apkItems

class ExecuteHelper():
    def __init__(self):
        
        self.uninstalllist = ['com.android.notepad', 'com.notepadblackboxtest']
        self.installlist = ['NotePad.apk', 'NotePadBlackBoxTest.apk']
        self.products = []

    def initProducts(self,jsonfile):
        if jsonfile:
            self.products = ParseProductJson(jsonfile).parse()
        else:
            #using default data
            if os.path.exists('devices.json'):
                self.products = ParseProductJson('devices.json').parse()
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

class TestTool(object):
    def __init__(self):
        pass

    def generatorLogfileName(self, testset):

        tmpstr = testset.replace('\\','/')
        testsetname = tmpstr.split('/')[-1]
        if len(testset) > 2:
            logfilename = "%s_%s%s"%(self.name,testsetname,'.log')
        return logfilename

class Instrument(TestTool):
    def __init__(self,commantTool, products,apkItems):

        self.name = 'Instrument'
        self.products = products
        self.apkItems = apkItems
        self.commandTool = commandTool
        #inclue apk info and parameters
        
    def run(self):
        
        for product in self.products:
            for apkItem in self.apkItems:

                instrumentCmd = ' -s ' + product.sn + ' uninstall ' + apkItem.package
                self.commandTool.runInstrument(instrumentCmd,'marble.log')
                instrumentCmd = ' -s ' + product.sn + ' uninstall ' + apkItem.testpackage
                self.commandTool.runInstrument(instrumentCmd,'marble.log')

                instrumentCmd = ' -s %s install %s'%(product.sn ,apkItem.apkName)
                self.commandTool.runInstrument(instrumentCmd,'marble.log')
                instrumentCmd = ' -s %s install %s'%(product.sn ,apkItem.testapk)
                self.commandTool.runInstrument(instrumentCmd,'marble.log')

            for product in self.products:
                for apkItem in self.apkItems:

                    instrumentCmd = ' -s %s shell am instrument -r -w %s/%s %s'%(product.sn, apkItem.testpackage, apkItem.runner, apkItem.parameters)
                    self.commandTool.runInstrument(instrumentCmd, 'Instrument.log')

class Marble(TestTool):
    def __init__(self,commandTool, marbleTool, products):

        self.name = "Marble"
        self.products = products
        self.marbleTool = marbleTool
        self.commandTool = commandTool
    def run(self,testset):

        print 'starting marble test ...'
        #copy marble to currentent
        if os.path.exists(self.marbleTool) and not os.path.exists('./marble'):
            shutil.copytree(self.marbleTool,'marble')
        print 'copy %s to %s' % (self.marbleTool,os.path.abspath('./marble'))
        #if os.path.exists('./marble'):
         #   shutil.copyfile('./execute.py', './marble/execute.py')

        print 'change work dir to %s'%os.path.abspath('./marble/framework')
        os.chdir('./marble/framework')
        for product in self.products:
            marbleCommand = " marble.py --connection %s --test_set %s"% (product.sn, testset)        
            self.commandTool.runMarble(marbleCommand, self.generatorLogfileName(testset))

def main(): 
    # Product list
    #step 1: parse the command line for products
    cmdparams = executeHelper.parseCmdLine()
    testmode = cmdparams.ensure_value('testmode', None)
    products = None
    if testmode:
        products = executeHelper.getProducts()
    else:
        product = cmdparams.ensure_value('product',None)
        products = executeHelper.initProducts(product)

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
    tool = commandTool(os.path.abspath('.'))
    logfile = cmdparams.ensure_value('logfile', None)

    #monkeytest
    Monkey = cmdparams.ensure_value('Monkey', None)
    if Monkey:
        compiledCommand =' -s '+products[0].sn +' shell monkey --throttle 500 -s 100 -v -v -v 1000'
        if logfile:
            tool.runMonkey(compiledCommand, 'Monkey.log')
        else:
            tool.runMonkey(compiledCommand, logfile)

    testset = cmdparams.ensure_value('testset',None)
    if testset:
        print 'testset is :%s' % testset
    else:
        print 'test set is none print input it'
    #marble test
    if not logfile:
        logfile = 'marble.log'
        print 'use default logfile:%s' % logfile

    marble = cmdparams.ensure_value("marble", None)
    if marble:
        marbletool = cmdparams.ensure_value('marbletool',None)
        marble = Marble(tool, marbletool, products)
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

        parseinstrument = ParseInstrumentJson()
        items = parseinstrument.parse(files)
        DisplayApkItems(items)

        instrument = Instrument(tool, products, items)
        Instrument.run()
                
    print 'finished'
if __name__ == '__main__': 
    main()

