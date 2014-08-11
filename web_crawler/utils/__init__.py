# -*- coding: utf-8 -*-
import datetime
import logging
import sys


class Debug():
    '''
    Debug info print( and write the log into files
    '''
    def __init__(self, logger=None, level=2):
        self.level = level
        self.logger = logger
        format = "[%(levelname)s][%(asctime)%s][%(message)s']\
[%(filename)s:%(funcName)s:%(lineno)s]"

        logging.basicConfig(filename=sys.argv[0]+".log",
                            level=logging.DEBUG,
                            filemode='w',
                            format=format)

    def formatLog(self, msg):
        '''
        Insert the time into line
        '''
        timeprefix = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return '[%s]%s' % (timeprefix, msg)

    def __call__(self, msg):
        self.debug(self.formatLog(msg))

    def debug(self, msg):
        msg = self.formatLog(msg)
        if self.level >= 3:
            print("Tool:Debug %s" % msg)
        if self.logger:
            self.logger.append(msg)

    def info(self, msg):
        msg = self.formatLog(msg)
        if self.level >= 2:
            print("Tool:Info %s" % msg)
        if self.logger:
            self.logger.append(msg)

    def error(self, msg):
        msg = self.formatLog(msg)
        if self.level >= 1:
            print("Tool:Error %s" % msg)
        if self.logger:
            self.logger.append(msg)

    def output(self, msg):
        msg = self.formatLog(msg)
        print('Tool:%s' % msg)
        if self.logger:
            self.logger.append(msg)
debug = Debug(level=3)


class CommandLine(object):
    def parseCmdLine(self):

        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-T', '--taskname', dest='TASKNAME',
                          help='build task name')

        parser.add_option('-p', '--product', dest='PRODUCT',
                          help='contains product information')

        parser.add_option('-s', '--supplier', dest='SUPPLIER',
                          help='company info  from supplier search page')

        parser.add_option('-w', '--website', dest='WEBSITE',
                          help='the website where the data will get from it')
        return parser.parse_args()



