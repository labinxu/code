from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
import login
import dlgnewtask
from mainwindow import Ui_MainWindow
import sys
if '../' not in sys.path:
    sys.path.append('../')
from manager.taskmanager import TaskManager
from typesdefine import Task, Enterprise
import threading
import time
from utils import debug


class DLGLogin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DLGLogin, self).__init__(parent)
        self.ui = login.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.edPasswd.setEchoMode(QtWidgets.QLineEdit.Password)

    @pyqtSlot()
    def on_btOk_clicked(self):
        self.accept()


##################################################################
class DLGNewTask(QtWidgets.QDialog):
    '''define the properties of the new task'''

    def __init__(self, parent=None):
        super(DLGNewTask, self).__init__(parent)
        self.ui = dlgnewtask.Ui_NewTask()
        self.ui.setupUi(self)
        self.ui.leTaskName.setText('task_1')
        self.ui.leSiteName.setText('ali')
        self.ui.leSearchWords.setText('keyboard')

    @pyqtSlot()
    def on_pbSearch_clicked(self):
        self.accept()


#################################################################
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tbwResult.setRowCount(10)
        self.ui.tbwResult.setColumnCount(7)
        self.runningTasksLocker = threading.Lock()
        self.stop = False
        self.tasks = []
        threading.Thread(target=self.taskMonitor,
                         args=(self.runningTasksLocker, )).start()

    def guiTasksMonitor(self):
        try:
            self.taskManager.resetDb('taskdb.sqlite3')
            print(Task.objects.all())
        except:
            pass
        
        try:
            self.taskManager.resetDb('task_1.db')
            for ent in Enterprise.objects.all():
                print(ent.company_name)
        except:
            pass

    @pyqtSlot()
    def on_actionLogin_triggered(self):
        # actionLogin
        dlgLogin = DLGLogin(self)
        dlgLogin.exec_()
        self.ui.ltOutput.addItem(dlgLogin.ui.edPasswd.text())
        self.ui.ltOutput.addItem(dlgLogin.ui.edUserName.text())

    def taskMonitor(self, locker):
        self.taskManager = TaskManager.Instance('taskdb.sqlite3')
        while not self.stop:
            debug.output('waiting task')
            if self.tasks:
                task = self.tasks.pop()
                task.save()
                self.taskManager.startTask(task)

            while self.taskManager.running_tasks:
                task, process = self.taskManager.running_tasks.popitem()
                if not process.is_alive():
                    task.task_status = '1'
                    task.save()
                    self.taskManager.completed_tasks.append(task)
                    self.guiTasksMonitor()
                else:
                    self.taskManager.running_tasks[task] = process
                time.sleep(2)
            time.sleep(2)

    @pyqtSlot()
    def on_actionNew_Task_triggered(self):
        dlgNewTask = DLGNewTask(self)
        dlgNewTask.exec_()
        searchWords = dlgNewTask.ui.leSearchWords.text()
        taskName = dlgNewTask.ui.leTaskName.text()
        siteName = dlgNewTask.ui.leSiteName.text()
        newTask = Task(task_name=taskName,
                       task_site_name=siteName,
                       task_search_words=searchWords,
                       task_status=0)

        self.ui.listRunningTasks.addItem(taskName)
        # self.runningTasksLocker.acquire()
        self.tasks.append(newTask)
        # self.runningTasksLocker.release()

    @pyqtSlot()
    def on_actionStop_triggered(self):
        self.stop = True

    @pyqtSlot()
    def on_actionStopAll_triggered(self):
        if self.stop:
            self.stop = False
            self.runningTasksLocker = threading.Lock()
            threading.Thread(target=self.taskMonitor,
                             args=(self.runningTasksLocker, )).start()

    @pyqtSlot()
    def on_actionInsert_triggered(self):
        newItem = QtWidgets.QTableWidgetItem('test')
        self.ui.tbwResult.setItem(1, 1, newItem)

    def itemChanged(self, row, col):
        self.ui.ltOutput.addItem('item %s, %s' % (col, row))

    def closeEvent(self, event):
        self.stop = True
        event.accept()

    def tabTasksClicked(self, index):
        debug.output('tab %s' % index)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
