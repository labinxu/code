import os,zipfile
class UtilsHelper():
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
        
        parser.add_option('-T','--testtype',dest = 'testtype',help = 'type of the test eg: marble ,instrument,Monkey...')
        
        #marble params
        parser.add_option('-A', '--marbletool',dest = 'marbletool',help ='marble tools name eg: ../marble.py')
        parser.add_option('-t', '--testset', dest ='testset', help='test case configure contains test case')
        
        #instrument params
        parser.add_option('-a', '--apk',dest = 'apk',help ='apk name')
        parser.add_option('-k', '--package',dest = 'package',help ='package name')
        parser.add_option('-e', '--testapk',dest = 'testapk',help ='testapk name')
        parser.add_option('-c', '--testpackage',dest = 'testpackage',help ='testpackage name')
        parser.add_option('-r', '--runner',dest = 'runner',help ='runner name')
        
        #Monkey command
        parser.add_option('-O', '--Monkey', dest = 'Monkey', help = 'Monkey test')
        
        parser.add_option('-P', '--parameters',dest = 'parameters',help ='marble tools name eg: ../marble.py')
        return parser.parse_args()

class Parse(object):
    
    def parse(self):
        return None
    def getJsonName(self, jsonfilename):
        return jsonfilename[0:-5]

class Logger:
    def __init__(self,dir,logfile):
        self.filename = logfile
        self.logfile = open(os.path.abspath(os.path.join(dir,logfile)),'w')
        self.workspace = dir
        
    def append(self,log):
        self.logfile.write(log)
        self.logfile.flush()
        
    def getdir(self,log):
        pass
    def store(self, workspace,compressFileName,zipConstruct):
        '''
        for example:
        workspace is : ./results/
        compressFileName is :result.zip
        the directory of result.zip is ../results
        the result.zip's files construction is result.zip/Marble/marble.log
        '''
        #the zip file will up one level by results folder 
        resultzip = os.path.abspath(os.path.join(workspace,'..',compressFileName))
        print 'compressing test results to %s' % resultzip
        preworkspace = os.path.abspath(os.getcwd())
        with zipfile.ZipFile(resultzip, 'a') as myzip:
            print 'change workspace to %s' % os.path.join(workspace)
            os.chdir(workspace)
            print 'adding %s/%s' % (zipConstruct,self.filename)                  
            myzip.write(os.path.join(zipConstruct,self.filename))
        print 'restore the workpace %s'%preworkspace
        os.chdir(preworkspace)
        self.logfile.close()

class JsonItem(object):
    def __init__(self):
        self.parameters = ""
        self.itemType = None
        self.itemName = None
        
    def displayAttributes(self):
        for name, value in vars(self).items():
            print '%s = %s'%(name, value)
            
class TestTool(object):
    def __init__(self):
        self.resultdirs = 'results'
        self.logName = 'result.log'
        self.compressName = 'result.zip'
        self.workspace = os.path.abspath(os.getcwd())
    def getResultdir(self):
        return self.resultdirs
    def prepareLogger(self,resultdirs):
        if not os.path.exists(resultdirs):
            print 'make dirs %s'%resultdirs
            os.makedirs(resultdirs)
        return Logger(resultdirs,self.logName)
    def run(self):
        pass
    def generatorLogfileName(self, testset):
        return "%s.log"%testset
