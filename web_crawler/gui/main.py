from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
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
    taskCompleted = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.taskManager = TaskManager()
        threading.Thread(target=self.guiMonitor,
                         args=()).start()
        self.taskManager.setDb('tasks.db')
        self.initResultView()
        self.taskResult = {}
        self.taskCompleted.connect(self.on_taskCompleted)

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
        pass

    @pyqtSlot()
    def on_actionStopAll_triggered(self):
        pass
        # self.runningTasksLocker = threading.Lock()
        # threading.Thread(target=self.taskMonitor,
        #                  args=(self.runningTasksLocker, )).start()

    @pyqtSlot()
    def on_actionInsert_triggered(self):
        newItem = QtWidgets.QTableWidgetItem('test')
        self.ui.tbwResult.setItem(1, 1, newItem)

    def itemChanged(self, row, col):
        # self.ui.ltOutput.addItem('item %s, %s' % (col, row))
        pass

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
        taskname = item.text()
        print('resetdb %s.db' % taskname)
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
        else:
            objects = self.taskResult[taskname]

        self.ui.tbwResult.setRowCount(len(objects))
        row = 0
        for ent in objects:
            for name, var in vars(ent).items():
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(var))
                self.ui.tbwResult.setItem(row, self.tabmap[name], item)
            row += 1


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
