# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\HandSight\src\qt_designer_files\settings_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settings_widget(object):
    def setupUi(self, settings_widget):
        settings_widget.setObjectName("settings_widget")
        settings_widget.resize(900, 600)
        self.splitter_2 = QtWidgets.QSplitter(settings_widget)
        self.splitter_2.setGeometry(QtCore.QRect(42, 50, 391, 480))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(10)
        self.splitter_2.setObjectName("splitter_2")
        self.device_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.device_label.setFont(font)
        self.device_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                        "color: rgb(217, 217, 217);\n"
                                        "border-radius:25px;")
        self.device_label.setAlignment(QtCore.Qt.AlignCenter)
        self.device_label.setObjectName("device_label")
        self.width_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.width_label.setFont(font)
        self.width_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                       "color: rgb(217, 217, 217);\n"
                                       "border-radius:25px;")
        self.width_label.setAlignment(QtCore.Qt.AlignCenter)
        self.width_label.setObjectName("width_label")
        self.height_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.height_label.setFont(font)
        self.height_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                        "color: rgb(217, 217, 217);\n"
                                        "border-radius:25px;")
        self.height_label.setAlignment(QtCore.Qt.AlignCenter)
        self.height_label.setObjectName("height_label")
        self.use_static_image_mode_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.use_static_image_mode_label.setFont(font)
        self.use_static_image_mode_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                                       "color: rgb(217, 217, 217);\n"
                                                       "border-radius:25px;")
        self.use_static_image_mode_label.setAlignment(QtCore.Qt.AlignCenter)
        self.use_static_image_mode_label.setObjectName("use_static_image_mode_label")
        self.min_detection_confidence_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.min_detection_confidence_label.setFont(font)
        self.min_detection_confidence_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                                          "color: rgb(217, 217, 217);\n"
                                                          "border-radius:25px;")
        self.min_detection_confidence_label.setAlignment(QtCore.Qt.AlignCenter)
        self.min_detection_confidence_label.setObjectName("min_detection_confidence_label")
        self.min_tracking_confidence_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.min_tracking_confidence_label.setFont(font)
        self.min_tracking_confidence_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                                         "color: rgb(217, 217, 217);\n"
                                                         "border-radius:25px;")
        self.min_tracking_confidence_label.setAlignment(QtCore.Qt.AlignCenter)
        self.min_tracking_confidence_label.setObjectName("min_tracking_confidence_label")
        self.use_brect_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setItalic(False)
        self.use_brect_label.setFont(font)
        self.use_brect_label.setStyleSheet("background-color: rgb(62, 65, 74);\n"
                                           "color: rgb(217, 217, 217);\n"
                                           "border-radius:25px;")
        self.use_brect_label.setAlignment(QtCore.Qt.AlignCenter)
        self.use_brect_label.setObjectName("use_brect_label")
        self.use_static_image_mode_checkbox = QtWidgets.QCheckBox(settings_widget)
        self.use_static_image_mode_checkbox.setGeometry(QtCore.QRect(470, 260, 390, 60))
        self.use_static_image_mode_checkbox.setStyleSheet("QCheckBox {\n"
                                                          "    background-color: rgb(62, 65, 74);\n"
                                                          "    color: rgb(217, 217, 217);\n"
                                                          "    border-radius: 25px;\n"
                                                          "}\n"
                                                          "QCheckBox::indicator  {\n"
                                                          " subcontrol-origin: border;\n"
                                                          "    subcontrol-position: center;\n"
                                                          "     width: 60px;\n"
                                                          "    height: 60px;\n"
                                                          "}")
        self.use_static_image_mode_checkbox.setText("")
        self.use_static_image_mode_checkbox.setChecked(True)
        self.use_static_image_mode_checkbox.setTristate(False)
        self.use_static_image_mode_checkbox.setObjectName("use_static_image_mode_checkbox")
        self.device_spinbox = QtWidgets.QSpinBox(settings_widget)
        self.device_spinbox.setGeometry(QtCore.QRect(470, 50, 390, 60))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(-1)
        self.device_spinbox.setFont(font)
        self.device_spinbox.setStyleSheet("QSpinBox {\n"
                                          "    background-color: rgb(62, 65, 74);\n"
                                          "    color: rgb(217, 217, 217);\n"
                                          "    border-radius: 25px;\n"
                                          "    font-family: \"Comic Sans MS\";\n"
                                          "    font-size: 20px;\n"
                                          "}\n"
                                          "QSpinBox::up-button  {\n"
                                          " subcontrol-origin: border;\n"
                                          "    subcontrol-position: top right;\n"
                                          "    min-width: 40px;\n"
                                          "    min_height: 25px;\n"
                                          "}\n"
                                          "QSpinBox::down-button  {\n"
                                          " subcontrol-origin: border;\n"
                                          "    subcontrol-position: bottom right;\n"
                                          "    min-width: 40px;\n"
                                          "    min_height: 25px;\n"
                                          "}\n"
                                          "QSpinBox::text {\n"
                                          "    padding-right: 20px;\n"
                                          "}\n"
                                          "")
        self.device_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.device_spinbox.setObjectName("device_spinbox")
        self.width_spinbox = QtWidgets.QSpinBox(settings_widget)
        self.width_spinbox.setGeometry(QtCore.QRect(470, 120, 390, 60))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(-1)
        self.width_spinbox.setFont(font)
        self.width_spinbox.setStyleSheet("QSpinBox {\n"
                                         "    background-color: rgb(62, 65, 74);\n"
                                         "    color: rgb(217, 217, 217);\n"
                                         "    border-radius: 25px;\n"
                                         "    font-family: \"Comic Sans MS\";\n"
                                         "    font-size: 20px;\n"
                                         "}\n"
                                         "QSpinBox::up-button  {\n"
                                         " subcontrol-origin: border;\n"
                                         "    subcontrol-position: top right;\n"
                                         "    min-width: 40px;\n"
                                         "    min_height: 25px;\n"
                                         "}\n"
                                         "QSpinBox::down-button  {\n"
                                         " subcontrol-origin: border;\n"
                                         "    subcontrol-position: bottom right;\n"
                                         "    min-width: 40px;\n"
                                         "    min_height: 25px;\n"
                                         "}\n"
                                         "")
        self.width_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.width_spinbox.setMaximum(5000)
        self.width_spinbox.setProperty("value", 960)
        self.width_spinbox.setObjectName("width_spinbox")
        self.height_spinbox = QtWidgets.QSpinBox(settings_widget)
        self.height_spinbox.setGeometry(QtCore.QRect(470, 190, 390, 60))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(-1)
        self.height_spinbox.setFont(font)
        self.height_spinbox.setStyleSheet("QSpinBox {\n"
                                          "    background-color: rgb(62, 65, 74);\n"
                                          "    color: rgb(217, 217, 217);\n"
                                          "    border-radius: 25px;\n"
                                          "    font-family: \"Comic Sans MS\";\n"
                                          "    font-size: 20px;\n"
                                          "}\n"
                                          "QSpinBox::up-button  {\n"
                                          " subcontrol-origin: border;\n"
                                          "    subcontrol-position: top right;\n"
                                          "    min-width: 40px;\n"
                                          "    min_height: 25px;\n"
                                          "}\n"
                                          "QSpinBox::down-button  {\n"
                                          " subcontrol-origin: border;\n"
                                          "    subcontrol-position: bottom right;\n"
                                          "    min-width: 40px;\n"
                                          "    min_height: 25px;\n"
                                          "}\n"
                                          "")
        self.height_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.height_spinbox.setMaximum(5000)
        self.height_spinbox.setProperty("value", 540)
        self.height_spinbox.setObjectName("height_spinbox")
        self.use_brect_checkbox = QtWidgets.QCheckBox(settings_widget)
        self.use_brect_checkbox.setGeometry(QtCore.QRect(470, 470, 390, 60))
        self.use_brect_checkbox.setStyleSheet("QCheckBox {\n"
                                              "    background-color: rgb(62, 65, 74);\n"
                                              "    color: rgb(217, 217, 217);\n"
                                              "    border-radius: 25px;\n"
                                              "}\n"
                                              "QCheckBox::indicator  {\n"
                                              " subcontrol-origin: border;\n"
                                              "    subcontrol-position: center;\n"
                                              "     width: 60px;\n"
                                              "    height: 60px;\n"
                                              "}")
        self.use_brect_checkbox.setText("")
        self.use_brect_checkbox.setChecked(True)
        self.use_brect_checkbox.setObjectName("use_brect_checkbox")
        self.min_detection_confidence_doublespinbox = QtWidgets.QDoubleSpinBox(settings_widget)
        self.min_detection_confidence_doublespinbox.setGeometry(QtCore.QRect(470, 330, 390, 60))
        self.min_detection_confidence_doublespinbox.setStyleSheet("QDoubleSpinBox {\n"
                                                                  "    background-color: rgb(62, 65, 74);\n"
                                                                  "    color: rgb(217, 217, 217);\n"
                                                                  "    border-radius: 25px;\n"
                                                                  "    font-family: \"Comic Sans MS\";\n"
                                                                  "    font-size: 20px;\n"
                                                                  "}\n"
                                                                  "QDoubleSpinBox::up-button  {\n"
                                                                  " subcontrol-origin: border;\n"
                                                                  "    subcontrol-position: top right;\n"
                                                                  "    min-width: 40px;\n"
                                                                  "    min_height: 25px;\n"
                                                                  "}\n"
                                                                  "QDoubleSpinBox::down-button  {\n"
                                                                  " subcontrol-origin: border;\n"
                                                                  "    subcontrol-position: bottom right;\n"
                                                                  "    min-width: 40px;\n"
                                                                  "    min_height: 25px;\n"
                                                                  "}\n"
                                                                  "")
        self.min_detection_confidence_doublespinbox.setDecimals(1)
        self.min_detection_confidence_doublespinbox.setMaximum(1.0)
        self.min_detection_confidence_doublespinbox.setSingleStep(0.1)
        self.min_detection_confidence_doublespinbox.setProperty("value", 0.5)
        self.min_detection_confidence_doublespinbox.setObjectName("min_detection_confidence_doublespinbox")
        self.min_tracking_confidence_doublespinbox = QtWidgets.QDoubleSpinBox(settings_widget)
        self.min_tracking_confidence_doublespinbox.setGeometry(QtCore.QRect(470, 400, 390, 60))
        self.min_tracking_confidence_doublespinbox.setStyleSheet("QDoubleSpinBox {\n"
                                                                 "    background-color: rgb(62, 65, 74);\n"
                                                                 "    color: rgb(217, 217, 217);\n"
                                                                 "    border-radius: 25px;\n"
                                                                 "    font-family: \"Comic Sans MS\";\n"
                                                                 "    font-size: 20px;\n"
                                                                 "}\n"
                                                                 "QDoubleSpinBox::up-button  {\n"
                                                                 " subcontrol-origin: border;\n"
                                                                 "    subcontrol-position: top right;\n"
                                                                 "    min-width: 40px;\n"
                                                                 "    min_height: 25px;\n"
                                                                 "}\n"
                                                                 "QDoubleSpinBox::down-button  {\n"
                                                                 " subcontrol-origin: border;\n"
                                                                 "    subcontrol-position: bottom right;\n"
                                                                 "    min-width: 40px;\n"
                                                                 "    min_height: 25px;\n"
                                                                 "}\n"
                                                                 "")
        self.min_tracking_confidence_doublespinbox.setDecimals(1)
        self.min_tracking_confidence_doublespinbox.setMaximum(1.0)
        self.min_tracking_confidence_doublespinbox.setSingleStep(0.1)
        self.min_tracking_confidence_doublespinbox.setProperty("value", 0.5)
        self.min_tracking_confidence_doublespinbox.setObjectName("min_tracking_confidence_doublespinbox")

        self.retranslateUi(settings_widget)
        QtCore.QMetaObject.connectSlotsByName(settings_widget)

    def retranslateUi(self, settings_widget):
        _translate = QtCore.QCoreApplication.translate
        settings_widget.setWindowTitle(_translate("settings_widget", "settings"))
        self.device_label.setText(_translate("settings_widget", "Устройство"))
        self.width_label.setText(_translate("settings_widget", "Ширина кадра"))
        self.height_label.setText(_translate("settings_widget", "Высота кадра"))
        self.use_static_image_mode_label.setText(_translate("settings_widget", "Поток жестов"))
        self.min_detection_confidence_label.setText(_translate("settings_widget", "Уверенность обнаружения"))
        self.min_tracking_confidence_label.setText(_translate("settings_widget", "Уверенность отслеживания"))
        self.use_brect_label.setText(_translate("settings_widget", "Отрисовка площади руки"))
