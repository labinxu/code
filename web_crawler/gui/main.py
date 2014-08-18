from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
import login
import dlgnewtask
from mainwindow import Ui_MainWindow
import sys
if '../' not in sys.path:
    sys.path.append('../')
from manager.taskmanager import TaskManager
from typesdefine import Task
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
        self.ui.leTaskName.setText('task 1')
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

    @pyqtSlot()
    def on_actionLogin_triggered(self):
        # actionLogin
        dlgLogin = DLGLogin(self)
        dlgLogin.exec_()
        self.ui.ltOutput.addItem(dlgLogin.ui.edPasswd.text())
        self.ui.ltOutput.addItem(dlgLogin.ui.edUserName.text())

    def newTask(self, locker, newTask):
        locker.acquire()
        self.taskManager = TaskManager.Instance('taskdb.sqlite3')
        self.taskManager.startTask(newTask)
        locker.release()
        while True:
            locker.acquire()
            status = self.taskManager.isAlive(newTask.task_name)
            locker.release()
            if not status:
                newTask.task_status = '1'
                newTask.save()
                debug.output('task %s finised' % newTask.task_name)
                break
            time.sleep(20)

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
        t = threading.Thread(target=self.newTask,
                             args=(self.runningTasksLocker, newTask))
        t.start()

    @pyqtSlot()
    def on_actionInsert_triggered(self):
        newItem = QtWidgets.QTableWidgetItem('test')
        self.ui.tbwResult.setItem(1, 1, newItem)

    def itemChanged(self, row, col):
        self.ui.ltOutput.addItem('item %s, %s' % (col, row))


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
