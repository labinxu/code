# -*- coding: utf-8 -*-


class Debug():
    def __init__(self, logger=None, level=2):
        self.level = level
        self.logger = logger

    def debug(self, msg):
        if self.level >= 3:
            print("Tool: Debug %s" % msg)
        if self.logger:
            self.logger.writeLine(msg)

    def info(self, msg):
        if self.level >= 2:
            print("Tool: Info %s" % msg)
        if self.logger:
            self.logger.writeLine(msg)

    def error(self, msg):
        if self.level >= 1:
            print("Tool: Error %s" % msg)
        if self.logger:
            self.logger.writeLine(msg)

    def output(self, msg):
        print('Tool: %s' % msg)
        if self.logger:
            self.logger.writeLine(msg)
debug = Debug()
