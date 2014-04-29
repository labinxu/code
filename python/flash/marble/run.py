#coding -*- utf-8 _8-
import sys,os,shutil,subprocess,time
sys.path.append('../')
from utils.utils import Parse,JsonItem,TestTool,Logger
def Start(products,filename, decodeJson):
    Marble(products,filename, decodeJson).run()
    #print 'run test case'
       
class MarbleItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)
        self.marbleTool = None
        self.testset = None
        
class MarbleJsonParser(Parse):
    def __init__(self,file= None):
        self.filename = file       
    def parse(self,decodeJson):
    
        item = MarbleItem()
        item.itemtype = decodeJson['type']
        item.itemName = self.getJsonName(self.filename)
        item.marbleTool = decodeJson[item.itemName][0]['marbleTool']
        item.testset =  decodeJson[item.itemName][0]['testset']
        item.parameters =  decodeJson[item.itemName][0]['parameters']       
        return [item]

class Marble(TestTool):
    def __init__(self, products,filename, decodeJson):
        TestTool.__init__(self)    
        self.name = "Marble"
        self.products = products
        self.testItems = MarbleJsonParser(filename).parse(decodeJson)
        self.workspace = os.path.abspath(os.getcwd())
        self.logdir = None
    def getCommand(self,toolArguments):
        command = 'ipy %s' % toolArguments
        return command  
    def generatorLogfileName(self, testset):
        tmpstr = testset.replace('\\','/')
        testsetname = tmpstr.split('/')[-1]
        if len(testset) > 2:
            logfilename = "%s_%s%s"%(self.name,testsetname,'.log')
        return logfilename    
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
        assert self.testItems
        marbleTool = self.testItems[0].marbleTool    
        if os.path.exists(marbleTool) and not os.path.exists('marble_tool'):
            print 'copy %s to %s' % (marbleTool,os.path.abspath('./marble_tool'))
            shutil.copytree(marbleTool,'marble_tool')
            
        print 'change work dir to %s'%os.path.abspath('./marble_tool/framework')
        os.chdir('./marble_tool/framework')
        for product in self.products:
            for item in self.testItems:
                self.logName = self.generatorLogfileName(item.testset)
                #./results/marble
                self.logdir = os.path.join(self.workspace,self.getResultdir(),self.name)
                logger = self.prepareLogger(self.logdir)
                toolArguments = " marble.py --connection %s --test_set %s %s"% (product.sn, item.testset, item.parameters)        
                self._run(logger,toolArguments)
                
                print 'workspace %s' %self.workspace
                logger.store(os.path.join(self.workspace,self.getResultdir()),self.compressName,self.name)