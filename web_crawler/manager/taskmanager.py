# -*- coding: utf-8 -*-
from db import DBHelper
import os
from typesdefine import Task
import importlib
from multiprocessing import Process


class TaskManager(object):
    _instance = None

    @staticmethod
    def Instance(taskdb=None):
        if not TaskManager._instance:
            TaskManager._instance = TaskManager(taskdb)
        return TaskManager._instance

    def __init__(self, taskdb):
        self.running_tasks = {}
        self.completed_tasks = []

        if not os.path.exists(taskdb):
            self.taskDb = DBHelper.getInstance(taskdb)
            self.taskDb.execute(Task.__init_table__)
        else:
            self.taskDb = DBHelper.getInstance(taskdb)

    def getSiteParser(self, siteName):
        module = importlib.import_module('sites.%s.main' % siteName)
        return module.GetParser()

    def getRunningTasks(self):
        return self.running_tasks

    def getCompletedTasks(self):
        return self.completed_tasks

    def startTask(self, task):
        crawler = self.getSiteParser(task.task_site_name)
        process = Process(target=crawler.startTask,
                          args=(task.task_name, task.task_search_words, None))
        process.start()
        self.running_tasks[task] = process

    def isAlive(self, task_name):
        if task_name in self.running_tasks.keys():
            return self.running_tasks[task_name].is_alive()
        else:
            return 0
