#coding -*- utf-8 _8-
import sys,os,shutil,subprocess,time
sys.path.append('../')
from utils.utils import Parse,JsonItem,TestTool,Logger
def Start(products,filename, decodeJson):
    Instrument(products,filename, decodeJson).run()

class InstrumentItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)
        self.apkName = None
        self.package = None
        self.testapk = None
        self.runner = None
class InstrumentJsonParser(Parse):
    def __init__(self, filename = None):
        self.filename = filename
    
    def parse(self,decodeJson):
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
    
    def parsefromfile(self,files):
        if isinstance(files,list):
            apkItems =[]
            for file in files:
                print 'parse file %s '%file
                apkItem = InstrumentItem()
                f = open(file)
                decodeJson = json.loads(f.read())
                f.close()
                apkItems.extend(parseObj(decodeJson))
            return apkItems
class Instrument(TestTool):
    def __init__(self, products,filename, decodeJson):
        TestTool.__init__(self)
        self.logName = 'result.log'
        self.workspace = os.path.abspath(os.getcwd())
        self.name = 'Instrument'
        self.products = products
        self.apkItems = InstrumentJsonParser(filename).parse(decodeJson)        
        #inclue apk info and parameters
    def setLogName(self, logName):
        self.logName = logName
        
    def prepareLogger(self,resultdirs):
        if not os.path.exists(resultdirs):
            os.makedirs(resultdirs)
        print 'log file %s'%os.path.join(resultdirs,self.logName)
        return Logger(resultdirs,self.logName)
    
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
                self.logdir = os.path.join(self.resultdirs,self.name)
                logger = self.prepareLogger(self.logdir)

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
                logger.store(os.path.join(self.workspace,self.getResultdir()),self.compressName,self.name)