# from
from utils.utils import utilsHelper, Flasher
utilsHelper.testMode = True
import os
if not os.path.exists('results'):
    os.makedirs('results')
flash = Flasher(utilsHelper, 3)
flash.flash()

maps = {1: 2, 2: 3}
   
if 1 in maps.keys():
    print 'ok'

def aa():
    cmd = 'adb -s %s shell pm disable com.nokia.FirstTimeUse\com.nokia.FirstTimeUse.Warranty' %\
          'aa'
    print cmd
aa()
