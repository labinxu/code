#coding utf-8

import execute,unittest, os

class TestExecute(unittest.TestCase):
    def testJson(self):
        try:
            products = execute.ParseJson('devices.json').parse()
            self.assertEqual(len(products),2)
        except Exception:
            print 'error'
            
    def testRunInterminal(self):
        self.assertTrue(os.system('python execute.py -j "devices.json"')==0)
        
    def testExecuteHelperforSN(self):
        product = execute.Product()
        product.sn ='111'
        execute.executeHelper.products.append(product)
        self.assertEqual(execute.executeHelper.getProductsSn(),['111'])
        
    def testtestMode(self):
        self.assertTrue(os.system('python execute.py --testmode')==0)
        
    def testcmdline(self):
        
        cmdparams = execute.executeHelper.parseCmdLine()
        ## instrument = cmdparams.ensure_value('instrument', None)
        ## testmode = cmdparams.ensure_value('testmode', None)
 
cmdparams = execute.executeHelper.parseCmdLine()

print cmdparams.ensure_value('instrument', None)

print cmdparams.ensure_value('testmode', None)
#unittest.main()
