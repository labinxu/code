# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Wed Aug 13 21:21:56 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(346, 260)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 311, 231))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lbUserName = QtWidgets.QLabel(self.groupBox)
        self.lbUserName.setGeometry(QtCore.QRect(40, 50, 64, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.lbUserName.setFont(font)
        self.lbUserName.setObjectName("lbUserName")
        self.lbPasswd = QtWidgets.QLabel(self.groupBox)
        self.lbPasswd.setEnabled(True)
        self.lbPasswd.setGeometry(QtCore.QRect(40, 120, 48, 18))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lbPasswd.setFont(font)
        self.lbPasswd.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lbPasswd.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.lbPasswd.setObjectName("lbPasswd")
        self.btOk = QtWidgets.QPushButton(self.groupBox)
        self.btOk.setGeometry(QtCore.QRect(50, 170, 72, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btOk.setFont(font)
        self.btOk.setObjectName("btOk")
        self.btCancel = QtWidgets.QPushButton(self.groupBox)
        self.btCancel.setGeometry(QtCore.QRect(190, 170, 72, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btCancel.setFont(font)
        self.btCancel.setObjectName("btCancel")
        self.edPasswd = QtWidgets.QLineEdit(self.groupBox)
        self.edPasswd.setGeometry(QtCore.QRect(110, 50, 161, 24))
        self.edPasswd.setInputMethodHints(QtCore.Qt.ImhNone)
        self.edPasswd.setObjectName("edPasswd")
        self.edUserName = QtWidgets.QLineEdit(self.groupBox)
        self.edUserName.setGeometry(QtCore.QRect(110, 120, 161, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.edUserName.setFont(font)
        self.edUserName.setObjectName("edUserName")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbUserName.setText(_translate("Dialog", "用户名："))
        self.lbPasswd.setText(_translate("Dialog", "密码："))
        self.btOk.setText(_translate("Dialog", "确认"))
        self.btCancel.setText(_translate("Dialog", "取消"))

