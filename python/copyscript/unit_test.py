#coding utf-8
import os
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
        self.assertTrue("android" in self.insTools.checkAppPath('adb','platform-tools'))
        self.assertTrue('bin' in self.insTools.checkAppPath('ruby'))
        self.assertFalse(self.insTools.checkAppPath('rubyerr'))

    def testGetAppdir(self):
        self.assertTrue('platform' in self.insTools.getAppdir(['%ANDROID_HOME%/platform-tools'],'adb'))
unittest.main()
    
