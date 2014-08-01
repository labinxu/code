# -*- coding: utf-8 -*-
import unittest
import sys
if '../' not in sys.path:
    sys.path.append('../')
import time


def print1():
    while(1):
        print(1)
        time.sleep(1)
def print2():
    while(1):
        time.sleep(1)
        print(2)
        

from utils.utils import Crawler
crawler = Crawler(print1)
crawler.start()
crawler2 = Crawler(print2)
crawler2.start()
crawler2.join(5)
crawler.join(5)
print('main thread')
crawler.stop()
crawler2.stop()
