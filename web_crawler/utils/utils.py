# -*- coding: utf-8 -*-

import threading


class Crawler(threading.Thread):
    def __init__(self, runner, timeout=None):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.runner = runner
        self.result = None

    def run(self):
        print('running...')
        self.result = self.runner()
