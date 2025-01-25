from PyQt5.QtWidgets import QWidget
from src.qt_designer_files.video_widget_base import Ui_video_widget

class VideoWidget(QWidget, Ui_video_widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)