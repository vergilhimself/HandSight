from PyQt5.QtWidgets import QWidget
from src.qt_designer_files.video_widget import Ui_Form  # Изменено здесь

class VideoWidget(QWidget, Ui_Form): # Изменено здесь
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)