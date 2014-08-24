import sys, time
if '../' not in sys.path:
    sys.path.append('../')
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from ui_mainform import Ui_main_frame


class MainFrame(QDialog):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)
        self.ui = Ui_main_frame()
        self.ui.setupUi(self)
        self.initResultView()

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
        
        print(self.ui.le_search_keywords.text())

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainFrame()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
