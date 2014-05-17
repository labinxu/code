#coding -*- utf-8 _8-
import sys,os,shutil
sys.path.append('../')
from utils.utils import Parse,JsonItem,TestTool,utilsHelper
import marble_result_parser

def Start(products,filename=None, decodeJson=None,items = None):
    if decodeJson:
        Marble(products,filename, decodeJson).run()
    else:
        Marble(products,filename,items = items).run()
    #print 'run test case'
def CreateItem(cmdparams):
    item = MarbleItem()
    item.itemType = "marble"
    item.itemName = item.itemType
    item.testset = cmdparams.testset and cmdparams.testset or ''    
    item.marbleTool = cmdparams.marbletool and cmdparams.marbletool or ''
    item.parameters = cmdparams.parameters and cmdparams.parameters or ''   
    return [item]
class MarbleItem(JsonItem):
    def __init__(self):
        JsonItem.__init__(self)
        self.marbleTool = None
        self.testset = None
class MarbleJsonParser(Parse):
    def __init__(self,file= None):
        self.filename = file       
    def parse(self,decodeJson):
        items = []
        itemType = decodeJson['type']
        itemName = self.getJsonName(self.filename)
        for subitem in decodeJson[itemName]:
            item = MarbleItem()
            item.itemType = itemType
            item.itemName = itemName
            item.marbleTool = subitem['marbleTool']
            item.testset =  subitem['testset']
            item.parameters =  subitem['parameters']       
            items.append(item)
        return items

class Marble(TestTool):
    def __init__(self, products,filename,decodeJson = None, items = None):
        TestTool.__init__(self)    
        self.name = "Marble"
        self.products = products
        if items:
            self.testItems = items
        else:
            self.testItems = MarbleJsonParser(filename).parse(decodeJson)
        self.workspace = os.path.abspath(os.getcwd())
        self.logdir = None
    def initSettingFile(self, product):
        #check the setting file
        if not os.path.exists('marble/settings/Main.xml'):
            print 'can not found marble/settings/Main.xml'
            return
        with open('marble/settings/Main.xml','r') as f:
            data = f.readlines()
            for i in range(len(data)):
                if 'name=' in data[i]:
                    beg = data[i].find('"')
                    end = data[i].rfind('"')
                    varName = data[i][beg+1:end]
                    if product.__dict__.has_key(varName):
                        data[i + 1] = '    <value type="string">%s</value>\n'%product.__dict__[varName]
                        i += 1
        #create a new setting file
        newf = open('Main.xml','w')
        for line in data:
            newf.write(line)
        newf.close()
        shutil.copy('Main.xml','marble/settings/Main.xml')
        
    def getCommand(self,toolArguments):
        command = 'ipy %s' % toolArguments
        return command  

    def generatorLogfileName(self, testset):
        tmpstr = testset.replace('\\','/')
        testsetname = tmpstr.split('/')[-1]
        if len(testset) > 2:
            logfilename = "%s_%s%s"%(self.name,testsetname,'.log')
        return logfilename

    def _run(self, logger, toolArguments):
        utilsHelper.unlockPhone(logger,self.currentProduct)
        utilsHelper.runCommand(logger,self.getCommand(toolArguments))
        
    def run(self):
        assert self.testItems
        #if the marble tool is not in current directory, should copy the marble  
        for product in self.products:
            self.currentProduct = product
            self.initSettingFile(product)
            for item in self.testItems:
                print 'change work dir from %s to %s'%(self.workspace, os.path.abspath('./marble/framework'))
                os.chdir('./marble/framework')
                self.logName = self.generatorLogfileName(item.testset)
                #./results/marble
                self.logdir = os.path.join(self.workspace,self.getResultdir(),self.name)
                logger = self.prepareLogger(self.logdir)
                toolArguments = " marble.py --connection %s --test_set %s %s"% (product.sn, item.testset, item.parameters)        
                self._run(logger,toolArguments)
                
                print 'workspace %s' %self.workspace
                #store the njunit framework/test_results/njunit/Marble_njunit.xml
                os.chdir(self.workspace)
                self._store(logger)
                #'marble/framework/test_results/njunit/Marble_njunit.xml'
            if os.path.exists('marble/framework/test_results'):
                import shutil
                print 'copy marbel_njunit.xml to results folder'
                if os.path.exists(os.path.join(self.getResultdir(),'njunit')):
                    shutil.rmtree(os.path.join(self.getResultdir(),'njunit'))
                utilsHelper.copyFolderContents('marble/framework/test_results',self.getResultdir())
                marble_result_parser.junitParser(os.path.join(self.getResultdir(),'njunit.xml'))
                utilsHelper.addDirArchive(self.resultzip,self.getResultdir())
            else:
                print "Tool: Error marble_njunit.xml have been found marble/framework/test_results/njunit"
