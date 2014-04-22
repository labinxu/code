#coding -*- utf-8 _8-

import os, sys, json, time, subprocess, zipfile

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
    
class ParseJson(Parse):

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

    
class ExecuteHelper():
    def __init__(self):
        
        self.uninstalllist = ['com.android.notepad', 'com.notepadblackboxtest']
        self.installlist = ['NotePad.apk', 'NotePadBlackBoxTest.apk']
        self.products = []

    def initProducts(self,jsonfile):
        if jsonfile:
            self.products = ParseJson(jsonfile).parse()
        else:
            #using default data
            self.products = ParseJson('devices.json').parse()
        return self.products

    def getProductsSn(self):
        return [product.sn for product in self.products]
    
    def getProducts(self):
        return self.products
    
    def parseCmdLine(self):
                
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-j', '--json', dest = 'jsonfile', help = 'contains product information')
        parser.add_option('-f', '--flash', dest = 'flashtool',help = 'flash tool name and path')
        parser.add_option('-t', '--testset', dest ='testset', help='test case configure contains test case')
        parser.add_option('-i',"--instrument",action='store_true' , help = 'instrument test')
        parser.add_option('-m', '--marble', action ='store_true',dest = 'marble', help ='marble test')
        parser.add_option('-M', '--Monkey', dest = 'Monkey', help = 'Monkey test')
        parser.add_option('-l', '--logfile', dest = 'logfile', help = 'log file save the result')
        parser.add_option('-T', '--testmode', dest ='testmode',action = 'store_false', help = 'for test mode for development')

        return parser.parse_args()[0]

executeHelper = ExecuteHelper()

def main(): 
    # Product list
    #step 1: parse the command line for products
    cmdparams = executeHelper.parseCmdLine()
    testmode = cmdparams.ensure_value('testmode', None)
    products = None
    if testmode:
        products = executeHelper.getProducts()
    else:
        jsonfile = cmdparams.ensure_value('jsonfile',None)
        products = executeHelper.initProducts(jsonfile)
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
    tool = commandTool('.')
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
        return 'test set is none'
    #marble test
    marble = cmdparams.ensure_value("marble", None)
    if marble:
        print 'starting marble test'
        marbleCommand = ' --test_set' + testset
        if logfile:
            tool.runMarble(marbleCommand,logfile)
        else:
            tool.runMarble(marbleCommand,'marble.log')

    #instrument test
    instrument = cmdparams.ensure_value('instrument', None)
    if not logfile:
        logfile = 'instrument.log'
        print 'use default logfile:%s' % logfile

    if instrument:
        print 'starting instrument testing ...'
        #install apk
        ## adb -s c2a4244 uninstall com.android.notepad                  *
        ## adb -s c2a4244 uninstall com.notepadblackboxtest
        ## adb -s c2a4244 install NotePad.apk                                         *
        ## adb -s c2a4244 install NotePadBlackBoxTest.apk
        for product in products:
            for uninstallapp in executeHelper.uninstalllist:
                instrumentCmd = ' -s ' + product.sn + ' uninstall ' + uninstallapp
                tool.runInstrument(instrumentCmd, logfile)
                print 'uninstall %s'%uninstallapp
                
            for installapp in executeHelper.installlist:
                instrumentCmd = ' -s ' + product.sn + ' install ' + installapp
                tool.runInstrument(instrumentCmd, logfile)
                print 'install %s' % installapp

        for product in products:
            instrumentCmd = ' -s ' + product.sn + ' shell am instrument -r -w '+ testset
            #run test case
            tool.runInstrument(instrumentCmd, logfile)

        #uninstall apk
        for product in products:
            for uninstallapp in executeHelper.uninstalllist:
                instrumentCmd = ' -s ' + product.sn + ' uninstall ' + uninstallapp
                tool.runInstrument(instrumentCmd, logfile)
        
    print 'finished'
if __name__ == '__main__': 
    main()

