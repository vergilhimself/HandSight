# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\HandSight\src\qt_designer_files\gestures_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import src.gui.resources_rc
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gestures_widget(object):
    def setupUi(self, gestures_widget):
        gestures_widget.setObjectName("gestures_widget")
        gestures_widget.resize(900, 600)
        gestures_widget.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.gesture_list = QtWidgets.QListWidget(gestures_widget)
        self.gesture_list.setGeometry(QtCore.QRect(10, 20, 491, 561))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.gesture_list.setFont(font)
        self.gesture_list.setObjectName("gesture_list")
        self.label = QtWidgets.QLabel(gestures_widget)
        self.label.setGeometry(QtCore.QRect(520, 30, 371, 91))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(gestures_widget)
        self.label_2.setGeometry(QtCore.QRect(520, 160, 371, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(gestures_widget)
        self.label_3.setGeometry(QtCore.QRect(520, 200, 371, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(gestures_widget)
        self.label_4.setGeometry(QtCore.QRect(520, 250, 361, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(gestures_widget)
        self.label_5.setGeometry(QtCore.QRect(510, 400, 381, 181))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/res/ASL_Alphabet_A_N.jpg"))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(gestures_widget)
        self.label_6.setGeometry(QtCore.QRect(520, 340, 371, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(gestures_widget)
        QtCore.QMetaObject.connectSlotsByName(gestures_widget)

    def retranslateUi(self, gestures_widget):
        _translate = QtCore.QCoreApplication.translate
        gestures_widget.setWindowTitle(_translate("gestures_widget", "Form"))
        self.label.setText(_translate("gestures_widget", "В данном окне вы можете привязать жест к дейсвтию на клавиатуре:"))
        self.label_2.setText(_translate("gestures_widget", "1. Нажмите на требуемый жест"))
        self.label_3.setText(_translate("gestures_widget", "2. Наведитесь мышью на диалоговое окно"))
        self.label_4.setText(_translate("gestures_widget", "3. Нажмите на клавишу или кнопку мыши"))
        self.label_6.setText(_translate("gestures_widget", "Жесты используются из букв алфавита A-N из ASL"))

