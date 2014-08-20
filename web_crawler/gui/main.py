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
import multiprocessing


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
        self.taskManager = TaskManager()
        threading.Thread(target=self.guiMonitor,
                         args=()).start()
        self.taskManager.setDb('tasks.db')
        self.stop = False

    def guiMonitor(self):
        while True:
            try:
                task = self.taskManager.popFinisedTask()
                if task is None:
                    pn = multiprocessing.current_process().name
                    print('end gui monitor %s' % pn)
                    break
                self.taskManager.resetDb('tasks.db')
                print('gui monitor task %s' % task.task_name)
                task.save()
            except:
                pass
            time.sleep(3)

    @pyqtSlot()
    def on_actionLogin_triggered(self):
        # actionLogin
        dlgLogin = DLGLogin(self)
        dlgLogin.exec_()
        self.ui.ltOutput.addItem(dlgLogin.ui.edPasswd.text())
        self.ui.ltOutput.addItem(dlgLogin.ui.edUserName.text())

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
        self.taskManager.addTask(newTask)

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
        self.taskManager.addTask(None)
        event.accept()

    def tabTasksClicked(self, index):
        if index == 1:
            self.taskManager.resetDb('tasks.db')
            self.ui.listCompletedTasks.clear()
            for task in Task.objects().filter('task_status="1"'):
                self.ui.listCompletedTasks.addItem(task.task_name)

    def completedTasksItemClicked(self, item):
        self.ui.ltOutput.addItem('select %s' % item.text())
        self.taskManager.resetDb('%s.db' % item.text())
        row = 0
        for ent in Enterprise.objects().all():
            column = 0
            for name, var in vars(ent).items():
                if name == 'id':
                    continue
                print('column %d, %s' % (column, name))
                #header = self.ui.tbwResult.horizontalHeaderItem(column)
                #header.setText(name)
               
                item = QtWidgets.QTableWidgetItem()
                item.setText(var)
                self.ui.tbwResult.setItem(row, column, item)
                column += 1
            row += 1
            self.ui.ltOutput.addItem(ent.company_name)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
