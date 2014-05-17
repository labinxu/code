from utils.utils import utilsHelper
from datetime import date
import time,threading, subprocess,os
import unittest
from marble.run import Marble
import execute
import shutil
def test_marble():
    products = execute.ParseProductJson('devices.json').parse()
    for product in products:
        product.displayAttributes()

class TestMarble(Marble):
    def __init__(self):
        pass
        def _run(self,logger,toolArguments):
            print toolArguments
            marble = TestMarble()
            marble.run()

print date.today()
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    import inspect,ctypes
    print 'terminal thread'
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble, 
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")

class FlashThread(threading.Thread):
    def __init__(self,identy):
        threading.Thread.__init__(self)
        self.identy = identy
        self.thread_stop = False
    
    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")
 
        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id
 
        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
 
        raise AssertionError("could not determine the thread's id")
    def run(self):
        while not self.thread_stop:
            print 'running...%s'%self.identy
            time.sleep(1)

    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        self.raise_exc(SystemExit)
        print 'terminate'
def testThread():
    thread1 = FlashThread('1')
    print 'start thread1'
    thread1.start()
    thread1.join(2)
    if thread1.isAlive():
        print 'alive() will kill it'
        thread1.terminate()
    print 'main thread'
    while(1):
        if thread1.isAlive():
            print 'still alive()'
            time.sleep(1)
        else:
            break
    print 'terminal main thread'
def run(self, command):
    exitcode = 0
    print 'run %s'%command
    try: 
        tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        toolOutputs = tool.stdout
        while 1: 
            outputFromTool = toolOutputs.readline() 
            time.sleep(1/10) 
            if not outputFromTool: 
                break 
            print 'Tool: ' + outputFromTool 
        exitcode = tool.wait()
        sys.stdout = sys.__stdout__
        print 'Tool execution finished' 
    except OSError, e:
        sys.stdout = sys.__stdout__
        print 'An error occured during execution: ', e 
        return exitcode

class CommandWatchCat(threading.Thread):
    def __init__(self, popen,timeout):
        threading.Thread.__init__(self)
        self.popen = popen
        self.timeout = timeout
    def run(self):
        time.sleep(self.timeout)
        print 'terminate command'
        self.popen.terminate()
        while not self.popen.poll():
            time.sleep(1)
            print 'wait kill'
class OBJ(object):
    pass
if not __name__=='__main__':
    print 'main'
    tool = subprocess.Popen('abc.bat', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    CommandWatchCat(tool,1).start()
    toolOutputs = tool.stdout
    while 1: 
        outputFromTool = toolOutputs.readline() 
        time.sleep(1/10) 
        if not outputFromTool: 
            break 
        print 'Tool: ' + outputFromTool
    print 'break while'
    exitcode = tool.wait()
    print exitcode
    exitcode -= 1
    print exitcode
    print 'main thread'
    
def testmmap():
    import mmap
    # write a simple example file
    with open("Main.xml", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        line = mm.readline()
        while line:
            line = mm.readline()
#            print line
            if 'name=' in line:
                print line
                line = mm.readline()
                print 'write'
                mm[0:2]="my"
            # read content via slice notation
#            print mm[:5]  # prints "Hello"
            # update content using slice notation;
            # note that new content must have same size
            # ... and read again using standard file methods
 #           mm.seek(0)
  #          print mm.readline()  # prints "Hello  world!"
            # close the map
        mm.close()
            
def testMakeMarbleSetting():
    products = execute.ParseProductJson('devices.json').parse()
    for p in products:
        print p.__dict__
        print type(vars(p).items())
    print 'prodct'
    if os.path.exists('marble/settings/Main.xml'):
        for p in products:
            with open('marble/settings/Main.xml','r') as f:
                data = f.readlines()
                for i in range(len(data)):
                    if 'name=' in data[i]:
                        beg = data[i].find('"')
                        end = data[i].rfind('"')
                        var = data[i][beg+1:end]
                        if p.__dict__.has_key(var):
                            data[i + 1] = '    <value type="string">%s</value>\n'%p.__dict__[var]
                            i += 1
        newf = open('Main.xml','w')
        for line in data:
            newf.write(line)
        newf.close()

        shutil.copy('Main.xml','marble/settings/Main.xml')
    else:
        print 'no file found'
if __name__=='__main__':
    testmmap()
