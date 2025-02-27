import sys
import mediapipe
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from gui.content_window import Ui_main_window
from funcs.video_processor import VideoProcessor
from gui.widgets import VideoWidget, SettingsWidget, GesturesWidget, LoginWidget
from funcs.navigation import NavigationManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.current_user_login = None  # Инициализация current_user_login

        self.login_widget = LoginWidget(self, self)  # создаем экземпляр LoginWidget и делаем его дочерним
        self.login_widget.setGeometry(0, 0, 1280, 720)  # на весь экран

        self.video_widget = VideoWidget()
        self.settings_widget = SettingsWidget()

        self.ui.functions_widget.addWidget(self.video_widget)
        self.ui.functions_widget.addWidget(self.settings_widget)

        self.navigation_manager = NavigationManager(self)

        self.ui.video_stream_button.clicked.connect(self.navigation_manager.show_video_widget)
        self.ui.settings_button.clicked.connect(self.navigation_manager.show_settings_widget)
        self.ui.gestures_button.clicked.connect(self.navigation_manager.show_gestures_widget)
        self.ui.exit_button.clicked.connect(self.navigation_manager.exit_app)

        self.video_processor = VideoProcessor()
        self.settings_widget.set_video_processor(self.video_processor)
        self.video_processor.frame_ready.connect(self.update_frame)
        self.video_processor.start()
        self.login_widget.show_login()  # Показываем логин виджет

    def set_current_user(self, current_user_login):
        print("Hello, user!")
        self.current_user_login = current_user_login
        self.navigation_manager.set_current_user(current_user_login)
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
