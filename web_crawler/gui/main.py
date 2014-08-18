from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from login import Ui_Dialog
from mainwindow import Ui_MainWindow


class DlgLogin(QtWidgets.QDialog):
    def __init__(self, parentWindow=None, parent=None):
        super(DlgLogin, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.edPasswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.parentWindow = parentWindow

    @pyqtSlot()
    def on_btOk_clicked(self):
        self.parentWindow.ui.ltOutput.addItem(self.ui.edUserName.text())
        self.accept()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tbwResult.setRowCount(10)
        self.ui.tbwResult.setColumnCount(7)

    @pyqtSlot()
    def on_actionLogin_triggered(self):
        # actionLogin
        dlgLogin = DlgLogin(self)
        dlgLogin.exec_()

    @pyqtSlot()
    def on_actionNew_Task_triggered(self):
        self.ui.listRunningTasks.addItem('xxx')

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
