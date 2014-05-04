#coding utf-8

import execute,unittest, os
import json,zipfile
class TestExecute(unittest.TestCase):
    def testJson(self):
        try:
            products = execute.ParseJson('devices.json').parse()
            self.assertEqual(len(products),2)
        except Exception:
            print 'error'
            
    def testRunInterminal(self):
        pass
#        self.assertTrue(os.system('python execute.py -p "devices.json"')==0)
        
    def testExecuteHelperforSN(self):
        product = execute.Product()
        product.sn ='111'
        execute.executeHelper.products.append(product)
        self.assertEqual(execute.executeHelper.getProductsSn(),['111'])
        
    def testtestMode(self):
        pass
#        self.assertTrue(os.system('python execute.py')==0)
        
    def testcmdline(self):
        
        cmdparams = execute.executeHelper.parseCmdLine()
        ## instrument = cmdparams.ensure_value('instrument', None)
        ## testmode = cmdparams.ensure_value('testmode', None)
    def testInstrumentJson(self):
        parseinstrument = execute.ParseInstrumentJson('rt_NotePad.json')

        items = parseinstrument.parse(['rt_NotePad.json'])
        if items:
            execute.DisplayApkItems(items)
    def testInstrumentJsonfromfile(self):
        f = open('rt_NotePad.json')
        jsonfile = json.loads(f.read())
        parseinstrument = execute.ParseInstrumentJson('rt_NotePad.json')
        items = parseinstrument.parseObj(jsonfile)
        self.assertEqual(len(items),1)
        
    def testcreatedirs(self):
        instrument = execute.Instrument(None,None)
        logger = instrument.prepareLogger('./results/notepad')
        data ='testhahah'
        self.assertEqual(logger.filename.replace('\\','/'),os.path.join(instrument.resultdirs,'notepad',instrument.logName).replace('\\','/'))
        logger.append(data)
        logger.append(data)
        logger.store('.','results.zip')
        self.assertTrue(os.path.exists('results.zip'))
        
        f = open('./results/notepad/result.log','r')
        line = f.read().replace('\n','')
        print line
        f.close()
        self.assertNotEqual(line,data)
    def testMarbleParse(self):
        f = open('marble_NotePad.json')
        decodeJson = json.loads(f.read())
        f.close()
        for item in execute.ParseMarbleJson("marble_NotePad.json").parseObj(decodeJson):
            print item.displayAttributes()
unittest.main()
