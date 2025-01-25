# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\HandSight\src\qt_designer_files\content_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import src.gui.resources_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1280, 720)
        main_window.setStyleSheet("background-color: rgb(62, 65, 74);")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 180, 220, 70))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 60, 181, 121))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/res/main_icon.svg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(95, 580, 190, 90))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setObjectName("splitter")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/res/vk_icon.svg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.splitter)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/res/tg_icon.svg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.actions = QtWidgets.QSplitter(self.centralwidget)
        self.actions.setGeometry(QtCore.QRect(60, 260, 260, 280))
        self.actions.setOrientation(QtCore.Qt.Vertical)
        self.actions.setHandleWidth(15)
        self.actions.setObjectName("actions")
        self.pushButton = QtWidgets.QPushButton(self.actions)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("    border-radius: 20px;\n"
"    background-color: rgb(217, 217, 217);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(self.actions)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("    border-radius: 20px;\n"
"    background-color: rgb(217, 217, 217);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.actions)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("    border-radius: 20px;\n"
"    background-color: rgb(217, 217, 217);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.actions)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("    border-radius: 20px;\n"
"    background-color: rgb(217, 217, 217);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.functions_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.functions_widget.setGeometry(QtCore.QRect(329, 59, 900, 600))
        self.functions_widget.setStyleSheet("background-color: rgb(217, 217, 217);\n"
"border-radius: 20px;")
        self.functions_widget.setObjectName("functions_widget")
        main_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(main_window)
        self.functions_widget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "HandSight - wanna see your gesture"))
        self.label.setText(_translate("main_window", "HandSight"))
        self.pushButton.setText(_translate("main_window", "PushButton"))
        self.pushButton_4.setText(_translate("main_window", "PushButton"))
        self.pushButton_3.setText(_translate("main_window", "PushButton"))
        self.pushButton_2.setText(_translate("main_window", "PushButton"))

