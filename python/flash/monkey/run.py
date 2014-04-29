#coding -*- utf-8 _8-
import sys,os,shutil,subprocess,time
sys.path.append('../')
from utils.utils import Parse,JsonItem,TestTool,Logger
def Start(products,filename, decodeJson):
    Monkey(products,filename, decodeJson).run()
    #print 'run test case'

class MonkeyItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)

class MonkeyJsonParser(Parse):
    def __init__(self, filename =None):
        self.filename = filename
    def parse(self, decodeJson):
        item = MonkeyItem()
        print decodeJson
        item.itemType = decodeJson['type']
        item.itemName = self.getJsonName(self.filename)
        item.parameters = decodeJson[item.itemName][0]['parameters']
        return [item]
class Monkey(TestTool):
    def __init__(self,products,filename, decodeJson):
        TestTool.__init__(self)
        self.resultdirs = './results'
        self.logName = 'Monkey.log'
        self.name = 'Monkey'
        self.products = products
        self.items = self.testItems = MonkeyJsonParser(filename).parse(decodeJson)
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
                logger = self.prepareLogger(os.path.join(self.resultdirs,self.name))
                toolArguments = ' -s '+product.sn +' shell monkey '+ item.parameters
                self._run(logger, toolArguments)
                logger.store(os.path.join(self.workspace,self.getResultdir()),self.compressName,self.name)