#coding utf-8
import debug
import installTools
insTools = installTools.SetUptools()

def test_checkEnv():
    if not insTools.checkEnv('ANDROID_HOME'):
        debug.debug('check ANDROID HOME FAILED')
        return
def test_checkAppPath():
    if not insTools.checkAppPath('adb','platform-tools'):
        debug.debug('check adb Failed')
    if not insTools.checkAppPath('ruby'):
        debug.debug('check ruby Failed')
           
def main():
    #step 1
    if not insTools.checkEnv('ANDROID_HOME'):
        return
    if not insTools.checkAppPath('adb','platform-tools'):
        return
    
if __name__ == '__main__':
    test_checkEnv()
    test_checkAppPath()
