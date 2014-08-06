import multiprocessing
import time


def func(msg, q):
    counter = 1
    while(1):
        q.put("done " + msg)
        time.sleep(2)
        counter += 1
        if counter == 4:
            print('ext')


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


class obj():
    def __init__(self, name):
        self.name = name
        self.output = OutPut()


def work(age):
    out = obj(age)
    return out


def main1():
    p = multiprocessing.Pool(processes=4)
    result = []
    for i in range(5):
        result.append(p.apply_async(work, args=(i,)))
    p.close()
    p.join()
    for r in result:
        print(r.get().name)

if __name__ == "__main__":
    main1()
