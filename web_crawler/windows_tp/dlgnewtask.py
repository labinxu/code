# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newtask.ui'
#
# Created: Mon Aug 18 10:26:37 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewTask(object):
    def setupUi(self, NewTask):
        NewTask.setObjectName("NewTask")
        NewTask.resize(735, 416)
        self.layoutWidget = QtWidgets.QWidget(NewTask)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 487, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.leTaskName = QtWidgets.QLineEdit(self.layoutWidget)
        self.leTaskName.setObjectName("leTaskName")
        self.horizontalLayout.addWidget(self.leTaskName)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.leSiteName = QtWidgets.QLineEdit(self.layoutWidget)
        self.leSiteName.setObjectName("leSiteName")
        self.horizontalLayout.addWidget(self.leSiteName)
        self.pbSwitchWebsite = QtWidgets.QPushButton(self.layoutWidget)
        self.pbSwitchWebsite.setObjectName("pbSwitchWebsite")
        self.horizontalLayout.addWidget(self.pbSwitchWebsite)
        self.leSearchWords = QtWidgets.QLineEdit(NewTask)
        self.leSearchWords.setGeometry(QtCore.QRect(30, 80, 113, 20))
        self.leSearchWords.setObjectName("leSearchWords")
        self.pbSearch = QtWidgets.QPushButton(NewTask)
        self.pbSearch.setGeometry(QtCore.QRect(170, 80, 75, 23))
        self.pbSearch.setObjectName("pbSearch")

        self.retranslateUi(NewTask)
        QtCore.QMetaObject.connectSlotsByName(NewTask)

    def retranslateUi(self, NewTask):
        _translate = QtCore.QCoreApplication.translate
        NewTask.setWindowTitle(_translate("NewTask", "Dialog"))
        self.label.setText(_translate("NewTask", "任务名称："))
        self.label_2.setText(_translate("NewTask", "站点名称："))
        self.pbSwitchWebsite.setText(_translate("NewTask", "切换站点"))
        self.pbSearch.setText(_translate("NewTask", "搜索"))

