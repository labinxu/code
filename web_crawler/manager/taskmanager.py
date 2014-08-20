# -*- coding: utf-8 -*-
from db import DBHelper
import os
import time
from typesdefine import Task
import importlib
from multiprocessing import Process, Queue
import psutil
import multiprocessing


class TaskManager(object):
    _instance = None

    def runningTaskMonitor(self):
        print('start running task monitor')
        print(multiprocessing.current_process().name)

        while True:
            task, pid = self.running_tasks.get()
            if task is None:
                pn = multiprocessing.current_process().name
                print('end running monitor %s' % pn)
                self.completed_tasks.put(None)
                break
            print('check %s id %s' % (task.task_name, pid))
            try:
                psutil.Process(pid)
            except psutil.NoSuchProcess:
                task.task_status = '1'
                self.completed_tasks.put(task)
                print('task %s finished' % task.task_name)
            else:
                self.running_tasks.put((task, pid))

            time.sleep(5)

    def popFinisedTask(self):
        return self.completed_tasks.get()

    def taskMonitor(self):
        print(multiprocessing.current_process().name)
        print('start task Monitor')
        while True:
            # TaskManager.newtask_cond.acquire()
            task = self.new_tasks.get()
            if task is None:
                pn = multiprocessing.current_process().name
                self.running_tasks.put((None, 0))
                break
            self.startTask(task)
            print('start task %s' % task.task_name)

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

        self.task_monitor = Process(target=self.taskMonitor, args=())
        self.task_monitor.start()
        self.running_monitor = Process(target=self.runningTaskMonitor,
                                       args=())
        self.running_monitor.start()

    def resetDb(self, dbname):
        self.taskDb.reset(dbname)

    def getSiteParser(self, siteName):
        module = importlib.import_module('sites.%s.main' % siteName)
        return module.GetParser()

    # def taskMonitor(self):
    #     while self.running_tasks:
    #         task, process = self.running_tasks.popitem()
    #         if not process.is_alive():
    #             task.task_status = '1'
    #             self.taskManager.completed_tasks.append(task)
    #         else:
    #             self.taskManager.running_tasks[task] = process

    def addTask(self, task):
        if task:
            print('add task %s' % task.task_name)
        self.new_tasks.put(task)
        
    def startTask(self, task):
        crawler = self.getSiteParser(task.task_site_name)
        p = Process(target=crawler.startTask,
                    args=(task.task_name, task.task_search_words, None))
        p.start()
        self.running_tasks.put((task, p.pid))
