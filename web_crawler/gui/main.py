from PyQt5 import QtWidgets
# from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtWidgets import QAction, QMenu
from login import Ui_Dialog
from mainwindow import Ui_MainWindow


class DlgLogin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DlgLogin, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.edPasswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.edUserName.setText('set text')
        # self.ui.btOk.clicked.connect(self.onOk)

    @pyqtSlot()
    def on_btOk_clicked(self):
        self.ui.lbUserName.setText(self.ui.edUserName.text())
        self.ui.lbPasswd.setText(self.ui.edPasswd.text())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
    @pyqtSlot()
    def on_actionLogin_triggered(self):
        # actionLogin
        dlgLogin = DlgLogin()
        dlgLogin.exec_()

    @pyqtSlot()
    def on_actionNew_Task_triggered(self):
        self.ui.listRunningTasks.addItem('xxx')
        


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
