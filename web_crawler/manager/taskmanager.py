# -*- coding: utf-8 -*-
from db import DBHelper
import os
import time
from typesdefine import Task
import importlib
from multiprocessing import Process, Queue, Value, Manager
import psutil
import sys
if '../' not in sys.path:
    sys.path.append('../')
from utils import debug


class TaskManager(object):
    _instance = None

    def runningTaskMonitor(self):
        debug.info('start running monitor')
        while True:
            task, pid = self.running_tasks.get()
            if task is None:
                self.completed_tasks.put(None)
                break
            try:
                psutil.Process(pid)
            except psutil.NoSuchProcess:
                task.task_status = '1'
                self.completed_tasks.put(task)
            else:
                self.running_tasks.put((task, pid))

            time.sleep(5)

    def taskMonitor(self):
        debug.info('start task monitor')

        while True:
            # TaskManager.newtask_cond.acquire()
            task = self.new_tasks.get()
            if task is None:
                self.running_tasks.put((None, 0))
                break
            debug.info('received task %s' % task.task_name)
            self.startTask(task, self.running_tasks_status)

    def startTask(self, task, progressStatus):
        crawler = self.getSiteParser(task.task_site_name)
        p = Process(target=crawler.startTask,
                    args=(task.task_name,
                          progressStatus,
                          task.task_search_words,
                          None))

        p.start()
        self.running_tasks.put((task, p.pid))

    def start(self):
        self.running_tasks_status = Manager().dict()
        self.startTaskMonitor()
        self.startRunningMonitor()

    def popFinisedTask(self):
        return self.completed_tasks.get()

    @staticmethod
    def Instance(taskdb=None):
        if not TaskManager._instance:
            TaskManager._instance = TaskManager(taskdb)
        return TaskManager._instance

    def setDb(self, taskdb):
        if not os.path.exists(taskdb):
            self.taskDb = DBHelper.getInstance(taskdb)
            self.taskDb.execute(Task.__init_table__)
        else:
            self.taskDb = DBHelper.getInstance(taskdb)

    def __init__(self):
        self.running_tasks = Queue()
        self.completed_tasks = Queue()
        self.new_tasks = Queue()
        self.running_tasks_status = None

    def checking(self):
        pass

    def startTaskMonitor(self):
        self.task_monitor = Process(target=self.taskMonitor, args=())
        self.task_monitor.start()

    def startRunningMonitor(self):
        self.running_monitor = Process(target=self.runningTaskMonitor,
                                       args=())
        self.running_monitor.start()

    def resetDb(self, dbname):
        self.taskDb.reset(dbname)

    def getSiteParser(self, siteName):
        module = importlib.import_module('sites.%s.main' % siteName)
        return module.GetParser()

    def addTask(self, task):
        self.new_tasks.put(task)

    def getRunningTask(self):
        task, pid = self.running_tasks.get()
