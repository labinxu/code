from multiprocessing import Queue, Process, Lock
import time


def func(msg, q):
    counter = 1
    while(1):
        q.put("done " + msg)
        time.sleep(2)
        counter += 1
        if counter == 4:
            print('ext')


def main():
    q = Queue()
    p = Process(target=func, args=('msg1', q))
    p.start()
    while True:
        time.sleep(1)
        print(q.get())


#################################
import os
class OutPut(object):
    def output(self, q):
        print('Output %s' % str(q))
        counter = 3
        while counter > 0:
            print('subprocess %s' % os.getpid())
            q.put(counter+1)
            time.sleep(2)
            counter -= 1
        print('subprocess exit')


def main1():
    q = Queue()
    out = OutPut()
    p = Process(target=out.output, args=(q, ))
    p.start()
    print('p pid %s ' % os.getpid())
    while True:
        if not q.empty():
            print(q.get())
        if not p.is_alive():
            print('main process exit')
            break

if __name__ == "__main__":
    main1()
