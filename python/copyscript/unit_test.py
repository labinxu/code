#coding utf-8
import debug
import unittest
import installTools

class TestEnv(unittest.TestCase):

    def setUp(self):
        self.insTools = installTools.SetUptools()
    def testCheckEnv(self):
        self.assertTrue(self.insTools.checkEnv('ANDROID_HOME'))
        self.assertFalse(self.insTools.checkEnv('noApp'))
                        
    def testCheckPath(self):
        self.assertTrue(self.insTools.checkAppPath('adb','platform-tools'))
        self.assertTrue(self.insTools.checkAppPath('ruby'))
        self.assertFalse(self.insTools.checkAppPath('rubyerr'))

if __name__ == '__main__':
    unittest.main()
    
