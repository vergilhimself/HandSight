from PyQt5.QtWidgets import QWidget
from src.qt_designer_files.video_widget_base import Ui_video_widget
from src.qt_designer_files.settings_widget_base import Ui_settings_widget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class VideoWidget(QWidget, Ui_video_widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def update_frame(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio))


class SettingsWidget(QWidget, Ui_settings_widget):
   def __init__(self, parent=None):
       super().__init__(parent)
       self.setupUi(self)

class GesturesWidget(QWidget, Ui_video_widget):
   def __init__(self, parent=None):
       super().__init__(parent)
       self.setupUi(self)