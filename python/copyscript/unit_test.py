import sys
from copytools import *
from environment import *
import shutil
e = CreateEnvhelper()
#e.append('path','d:\\test2')
#print e.getenv('path')
#print checkEnv('ANDROID_HOME')
if os.path.exists(os.path.join(os.path.expanduser('~'),'.android1')):
    print 'exit'
else:
    os.system('mkdir %s'%os.path.join(os.path.expanduser('~'),'.android1'))
    print 'not exit'





