# D:\Projects\HandSight\src\main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from src.gui.content_window import Ui_main_window
from src.funcs.video_processor import VideoProcessor
from src.gui.widgets import VideoWidget, SettingsWidget, GesturesWidget
from src.funcs.navigation import NavigationManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.video_widget = VideoWidget()
        self.settings_widget = SettingsWidget()
        # self.gestures_widget = GesturesWidget() # Теперь создается в NavigationManager

        self.ui.functions_widget.addWidget(self.video_widget)
        self.ui.functions_widget.addWidget(self.settings_widget)
        # self.ui.functions_widget.addWidget(self.gestures_widget) # Теперь добавляется в NavigationManager

        self.navigation_manager = NavigationManager(self)

        self.ui.video_stream_button.clicked.connect(self.navigation_manager.show_video_widget)
        self.ui.settings_button.clicked.connect(self.navigation_manager.show_settings_widget)
        self.ui.gestures_button.clicked.connect(self.navigation_manager.show_gestures_widget) # Подключение к новому методу
        self.ui.exit_button.clicked.connect(self.navigation_manager.exit_app) # Подключение кнопки выхода

        self.video_processor = VideoProcessor()
        self.video_processor.frame_ready.connect(self.update_frame)
        self.video_processor.start()

        self.navigation_manager.show_video_widget()

    def update_frame(self, frame):
        if self.ui.functions_widget.currentWidget() == self.video_widget:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            self.video_widget.video_label.setPixmap(
                pixmap.scaled(self.video_widget.video_label.size(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.video_processor.stop()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())