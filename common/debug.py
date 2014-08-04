# -*- coding: utf-8 -*-
import datetime


class Debug():
    '''
    Debug info print( and write the log into files
    '''
    def __init__(self, logger=None, level=2):
        self.level = level
        self.logger = logger

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

