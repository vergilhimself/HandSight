from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_gestures_widget(object):
    def setupUi(self, video_widget):
        video_widget.setObjectName("video_widget")
        video_widget.resize(900, 600)
        self.video_label = QtWidgets.QLabel(video_widget)
        self.video_label.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.video_label.setText("")
        self.video_label.setObjectName("video_label")

        self.retranslateUi(video_widget)
        QtCore.QMetaObject.connectSlotsByName(video_widget)

    def retranslateUi(self, video_widget):
        _translate = QtCore.QCoreApplication.translate
        video_widget.setWindowTitle(_translate("video_widget", "Form"))