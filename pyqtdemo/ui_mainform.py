# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainframe.ui'
#
# Created: Sun Aug 24 16:00:59 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_frame(object):
    def setupUi(self, main_frame):
        main_frame.setObjectName("main_frame")
        main_frame.resize(716, 571)
        self.tbwg_menubar = QtWidgets.QTabWidget(main_frame)
        self.tbwg_menubar.setGeometry(QtCore.QRect(10, 60, 691, 501))
        self.tbwg_menubar.setObjectName("tbwg_menubar")
        self.newtask = QtWidgets.QWidget()
        self.newtask.setObjectName("newtask")
        self.le_search_keywords = QtWidgets.QLineEdit(self.newtask)
        self.le_search_keywords.setGeometry(QtCore.QRect(70, 70, 131, 20))
        self.le_search_keywords.setObjectName("le_search_keywords")
        self.pb_new_task = QtWidgets.QPushButton(self.newtask)
        self.pb_new_task.setGeometry(QtCore.QRect(470, 430, 75, 23))
        self.pb_new_task.setObjectName("pb_new_task")
        self.lb_search_conditions = QtWidgets.QLabel(self.newtask)
        self.lb_search_conditions.setGeometry(QtCore.QRect(10, 70, 54, 12))
        self.lb_search_conditions.setObjectName("lb_search_conditions")
        self.toolButton = QtWidgets.QToolButton(self.newtask)
        self.toolButton.setGeometry(QtCore.QRect(160, 20, 37, 18))
        self.toolButton.setObjectName("toolButton")
        self.lb_current_site = QtWidgets.QLabel(self.newtask)
        self.lb_current_site.setGeometry(QtCore.QRect(70, 20, 91, 16))
        self.lb_current_site.setObjectName("lb_current_site")
        self.lb_task_name = QtWidgets.QLabel(self.newtask)
        self.lb_task_name.setGeometry(QtCore.QRect(250, 20, 60, 16))
        self.lb_task_name.setObjectName("lb_task_name")
        self.leTaskName = QtWidgets.QLineEdit(self.newtask)
        self.leTaskName.setGeometry(QtCore.QRect(310, 20, 133, 20))
        self.leTaskName.setObjectName("leTaskName")
        self.lb_site_name = QtWidgets.QLabel(self.newtask)
        self.lb_site_name.setGeometry(QtCore.QRect(10, 20, 60, 16))
        self.lb_site_name.setObjectName("lb_site_name")
        self.pbSwitchWebsite = QtWidgets.QPushButton(self.newtask)
        self.pbSwitchWebsite.setGeometry(QtCore.QRect(550, 430, 75, 23))
        self.pbSwitchWebsite.setObjectName("pbSwitchWebsite")
        self.tbwg_menubar.addTab(self.newtask, "")
        self.processing_tasks = QtWidgets.QWidget()
        self.processing_tasks.setObjectName("processing_tasks")
        self.gb_processing_tasks = QtWidgets.QGroupBox(self.processing_tasks)
        self.gb_processing_tasks.setGeometry(QtCore.QRect(10, 10, 171, 461))
        self.gb_processing_tasks.setObjectName("gb_processing_tasks")
        self.lw_processing_tasks = QtWidgets.QListWidget(self.gb_processing_tasks)
        self.lw_processing_tasks.setGeometry(QtCore.QRect(10, 20, 151, 431))
        self.lw_processing_tasks.setObjectName("lw_processing_tasks")
        self.gb_processing_task_details = QtWidgets.QGroupBox(self.processing_tasks)
        self.gb_processing_task_details.setGeometry(QtCore.QRect(190, 10, 491, 461))
        self.gb_processing_task_details.setObjectName("gb_processing_task_details")
        self.tw_processing_task_details = QtWidgets.QTableWidget(self.gb_processing_task_details)
        self.tw_processing_task_details.setGeometry(QtCore.QRect(10, 20, 471, 431))
        self.tw_processing_task_details.setObjectName("tw_processing_task_details")
        self.tw_processing_task_details.setColumnCount(0)
        self.tw_processing_task_details.setRowCount(0)
        self.tbwg_menubar.addTab(self.processing_tasks, "")
        self.finished_tasks = QtWidgets.QWidget()
        self.finished_tasks.setObjectName("finished_tasks")
        self.gb_finished_task_details = QtWidgets.QGroupBox(self.finished_tasks)
        self.gb_finished_task_details.setGeometry(QtCore.QRect(190, 10, 491, 461))
        self.gb_finished_task_details.setObjectName("gb_finished_task_details")
        self.tw_finished_task_details = QtWidgets.QTableWidget(self.gb_finished_task_details)
        self.tw_finished_task_details.setGeometry(QtCore.QRect(10, 20, 471, 431))
        self.tw_finished_task_details.setObjectName("tw_finished_task_details")
        self.tw_finished_task_details.setColumnCount(0)
        self.tw_finished_task_details.setRowCount(0)
        self.gb_finished_tasks = QtWidgets.QGroupBox(self.finished_tasks)
        self.gb_finished_tasks.setGeometry(QtCore.QRect(10, 10, 171, 461))
        self.gb_finished_tasks.setObjectName("gb_finished_tasks")
        self.lw_finished_tasks = QtWidgets.QListWidget(self.gb_finished_tasks)
        self.lw_finished_tasks.setGeometry(QtCore.QRect(10, 20, 151, 431))
        self.lw_finished_tasks.setObjectName("lw_finished_tasks")
        self.tbwg_menubar.addTab(self.finished_tasks, "")
        self.history_tasks = QtWidgets.QWidget()
        self.history_tasks.setObjectName("history_tasks")
        self.gb_date = QtWidgets.QGroupBox(self.history_tasks)
        self.gb_date.setGeometry(QtCore.QRect(10, 10, 141, 431))
        self.gb_date.setObjectName("gb_date")
        self.tbwg_menubar.addTab(self.history_tasks, "")
        self.pushButton = QtWidgets.QPushButton(main_frame)
        self.pushButton.setGeometry(QtCore.QRect(200, 10, 75, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(main_frame)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 10, 75, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(main_frame)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 10, 75, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gv_logon = QtWidgets.QGraphicsView(main_frame)
        self.gv_logon.setGeometry(QtCore.QRect(10, 10, 181, 41))
        self.gv_logon.setObjectName("gv_logon")

        self.retranslateUi(main_frame)
        self.tbwg_menubar.setCurrentIndex(0)
        self.pb_new_task.clicked.connect(main_frame.on_new_task_clicked)
        QtCore.QMetaObject.connectSlotsByName(main_frame)

    def retranslateUi(self, main_frame):
        _translate = QtCore.QCoreApplication.translate
        main_frame.setWindowTitle(_translate("main_frame", "启通"))
        self.pb_new_task.setText(_translate("main_frame", "确定"))
        self.lb_search_conditions.setText(_translate("main_frame", "搜索条件："))
        self.toolButton.setText(_translate("main_frame", "..."))
        self.lb_current_site.setText(_translate("main_frame", "TextLabel"))
        self.lb_task_name.setText(_translate("main_frame", "任务名称："))
        self.lb_site_name.setText(_translate("main_frame", "站点名称："))
        self.pbSwitchWebsite.setText(_translate("main_frame", "清空"))
        self.tbwg_menubar.setTabText(self.tbwg_menubar.indexOf(self.newtask), _translate("main_frame", "新建任务"))
        self.gb_processing_tasks.setTitle(_translate("main_frame", "任务列表"))
        self.gb_processing_task_details.setTitle(_translate("main_frame", "任务详情"))
        self.tbwg_menubar.setTabText(self.tbwg_menubar.indexOf(self.processing_tasks), _translate("main_frame", "未完成"))
        self.gb_finished_task_details.setTitle(_translate("main_frame", "任务详情"))
        self.gb_finished_tasks.setTitle(_translate("main_frame", "任务列表"))
        self.tbwg_menubar.setTabText(self.tbwg_menubar.indexOf(self.finished_tasks), _translate("main_frame", "已完成"))
        self.gb_date.setTitle(_translate("main_frame", "日期"))
        self.tbwg_menubar.setTabText(self.tbwg_menubar.indexOf(self.history_tasks), _translate("main_frame", "历史"))
        self.pushButton.setText(_translate("main_frame", "登陆"))
        self.pushButton_3.setText(_translate("main_frame", "编辑"))
        self.pushButton_4.setText(_translate("main_frame", "帮助"))
