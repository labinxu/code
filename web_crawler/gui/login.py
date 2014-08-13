# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Wed Aug 13 13:25:23 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(350, 224)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.edPasswd = QtWidgets.QLineEdit(Dialog)
        self.edPasswd.setGeometry(QtCore.QRect(140, 100, 113, 20))
        self.edPasswd.setInputMethodHints(QtCore.Qt.ImhNone)
        self.edPasswd.setObjectName("edPasswd")
        self.lbPasswd = QtWidgets.QLabel(Dialog)
        self.lbPasswd.setEnabled(True)
        self.lbPasswd.setGeometry(QtCore.QRect(60, 100, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lbPasswd.setFont(font)
        self.lbPasswd.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lbPasswd.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.lbPasswd.setObjectName("lbPasswd")
        self.edUserName = QtWidgets.QLineEdit(Dialog)
        self.edUserName.setGeometry(QtCore.QRect(140, 50, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.edUserName.setFont(font)
        self.edUserName.setObjectName("edUserName")
        self.lbUserName = QtWidgets.QLabel(Dialog)
        self.lbUserName.setGeometry(QtCore.QRect(60, 50, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.lbUserName.setFont(font)
        self.lbUserName.setObjectName("lbUserName")
        self.btOk = QtWidgets.QPushButton(Dialog)
        self.btOk.setGeometry(QtCore.QRect(80, 150, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btOk.setFont(font)
        self.btOk.setObjectName("btOk")
        self.btCancel = QtWidgets.QPushButton(Dialog)
        self.btCancel.setGeometry(QtCore.QRect(180, 150, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btCancel.setFont(font)
        self.btCancel.setObjectName("btCancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbPasswd.setText(_translate("Dialog", "密码："))
        self.lbUserName.setText(_translate("Dialog", "用户名："))
        self.btOk.setText(_translate("Dialog", "确认"))
        self.btCancel.setText(_translate("Dialog", "取消"))

