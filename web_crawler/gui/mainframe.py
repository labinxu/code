# !/usr/bin/env python  
# coding=utf-8
import sys
import time
import threading
if '../' not in sys.path:
    sys.path.append('../')
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from ui_templates.ui_mainform import Ui_main_frame
from manager.taskmanager import TaskManager
from typesdefine import Task, Enterprise
from utils import debug

from multiprocessing import freeze_support
# for cx_freeze fixed
sys.stdout = open('mainframe.log', 'w')
sys.stderr = sys.stdout
freeze_support()


class MainFrame(QDialog):
    signalTaskCompleted = pyqtSignal(str)
    signalCreatedSuccessful = pyqtSignal()

    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)
        self.ui = Ui_main_frame()
        self.ui.setupUi(self)
        self.initResultView()
        self.taskManager = None
        self.taskResult = {}
        threading.Thread(target=self.guiMonitor, args=()).start()
        self.signalTaskCompleted.connect(self.onTaskCompleted)
        self.signalCreatedSuccessful.connect(self.onCreatedSuccessful)
        self.signalCreatedSuccessful.emit()

    def onCreatedSuccessful(self):
        debug.info('Main Frame created')
        self.initTaskManager()

    def initTaskManager(self):
        # task relations
        self.taskManager = TaskManager()
        self.taskManager.setDb('tasks.db')
        self.taskManager.startTaskMonitor()
        self.taskManager.startRunningMonitor()

    def initResultView(self):
        self.tabmap = {}
        self.tabmap["company_name"] = 0
        self.tabmap["company_contacts"] = 1
        self.tabmap["company_phone_number"] = 2
        self.tabmap["company_mobile_phone"] = 3
        self.tabmap["company_fax"] = 4
        self.tabmap["company_postcode"] = 5
        self.tabmap["company_website"] = 6
        self.tabmap["company_addr"] = 7
        self.tabmap["company_details"] = 8
        self.tabmap['id'] = 9

    def guiMonitor(self):
        debug.info('start gui monitor')
        while True:
            try:
                task = self.taskManager.popFinisedTask()
                if task is None:
                    break
                self.taskManager.resetDb('tasks.db')
                debug.info('gui monitor %s finised' % task.task_name)
                self.signalTaskCompleted.emit(task.task_name)
                task.save()
            except:
                pass
            time.sleep(3)

    def onLWFinishedTasksClicked(self, item):
        taskname = item.text()
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
        else:
            objects = self.taskResult[taskname]

        self.ui.tw_finished_task_details.setRowCount(len(objects))
        row = 0
        for ent in objects:
            for name, var in vars(ent).items():
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(var))
                self.ui.tw_finished_task_details.setItem(row,
                                                         self.tabmap[name],
                                                         item)
            row += 1

    def onTaskCompleted(self, taskname):
        debug.info('task %s finished' % taskname)
        model = self.ui.lw_processing_tasks.model()
        for i in range(self.ui.lw_processing_tasks.count()):
            item = self.ui.lw_processing_tasks.item(i)
            if item.text() == taskname:
                model.removeRow(i)
                self.ui.lw_finished_tasks.addItem(taskname)
                break

    def onNewTaskClicked(self):
        '''Create a new task'''
        msginfo = 'New Task clicked'
        self.ui.lw_output.addItem(msginfo)

        taskName = self.ui.le_task_name.text()
        siteName = self.ui.lb_current_site.text()
        keyWords = self.ui.le_search_keywords.text()
        if not (taskName and siteName and keyWords):
            return
        msginfo = 'New task %s,%s,%s' % (taskName, siteName, keyWords)
        debug.info(msginfo)
        self.ui.lw_output.addItem(msginfo)

        newTask = Task(task_name=taskName,
                       task_site_name=siteName,
                       task_search_words=keyWords,
                       task_status=0)
        self.ui.lw_processing_tasks.addItem(taskName)
        self.taskManager.addTask(newTask)

    def closeEvent(self, event):
        debug.info('received close evnet')
        self.taskManager.addTask(None)
        event.accept()


def main():
    import sys
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MainFrame()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
