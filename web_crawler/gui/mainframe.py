#!/usr/bin/env python  
#coding=utf-8
import sys, time
import sip, re
import threading
if '../' not in sys.path:
    sys.path.append('../')
import PyQt5
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_templates.ui_mainform import Ui_main_frame
from manager.taskmanager import TaskManager
from typesdefine import Task, Enterprise


class MainFrame(QDialog):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)
        self.ui = Ui_main_frame()
        self.ui.setupUi(self)
        self.initResultView()
        # task relations
        self.taskManager = TaskManager()
        threading.Thread(target=self.guiMonitor, args=()).start()
        self.taskManager.setDb('tasks.db')
        self.taskResult = {}

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
        while True:
            try:
                task = self.taskManager.popFinisedTask()
                if task is None:
                    break
                self.taskManager.resetDb('tasks.db')
                self.taskCompleted.emit(task.task_name)
                task.save()
            except:
                pass
            time.sleep(3)

    def on_taskCompleted(self, taskname):
        model = self.ui.listRunningTasks.model()
        for i in range(self.ui.listRunningTasks.count()):
            item = self.ui.listRunningTasks.item(i)
            if item.text() == taskname:
                print('find %s' % taskname)
                model.removeRow(i)
                break

    def on_new_task_clicked(self):

        taskName = self.ui.le_task_name.text()
        siteName = self.ui.lb_current_site.text()
        keyWords = self.ui.le_search_keywords.text()
        
        if not (taskName and siteName and keyWords):
            return
        self.ui.lw_output.addItem('%s,%s,%s' % (taskName, siteName, keyWords))
        newTask = Task(task_name=taskName,
                       task_site_name=siteName,
                       task_search_words=keyWords,
                       task_status=0)
        self.ui.lw_processing_tasks.addItem(taskName)
        self.taskManager.addTask(newTask)

    def closeEvent(self, event):
        print('close event')
        self.taskManager.addTask(None)
        event.accept()


def main():
    import sys
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    app.addLibraryPath('.')
    window = MainFrame()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
