import mediapipe as mp
import sys
import sqlite3
import os  # Импортируем модуль os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from gui.content_window import Ui_main_window
from funcs.video_processor import VideoProcessor
from gui.widgets import VideoWidget, SettingsWidget, GesturesWidget, LoginWidget
from funcs.navigation import NavigationManager
from src.funcs.db_funcs import get_user_gesture_bindings, create_user_gesture_bindings_table, save_user_gesture_binding

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.current_user_id = None  # Initialize current_user_id

        self.login_widget = LoginWidget(self, self)
        self.login_widget.setGeometry(0, 0, 1280, 720)

        self.video_widget = VideoWidget()
        self.settings_widget = SettingsWidget()

        self.ui.functions_widget.addWidget(self.video_widget)
        self.ui.functions_widget.addWidget(self.settings_widget)

        self.navigation_manager = NavigationManager(self)

        self.ui.video_stream_button.clicked.connect(self.navigation_manager.show_video_widget)
        self.ui.settings_button.clicked.connect(self.navigation_manager.show_settings_widget)
        self.ui.gestures_button.clicked.connect(self.navigation_manager.show_gestures_widget)
        self.ui.exit_button.clicked.connect(self.navigation_manager.exit_app)

        # Database path
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "handsight.db")
        print(f"Database path: {self.db_path}")  # Проверяем, что путь к БД верный
        create_user_gesture_bindings_table(self.db_path)  # Ensure table exists

        #  DO NOT start VideoProcessor in __init__. Start it after login.
        self.video_processor = None # Initialize to None
        self.settings_widget.set_video_processor(None) # also set to None
        self.login_widget.show_login()  # Show the login widget

    def set_current_user(self, current_user_id):
        print(f"Установлен текущий пользователь: {current_user_id}")
        self.current_user_id = current_user_id
        self.navigation_manager.set_current_user(current_user_id)

    def get_current_gesture_key_map(self):
        """Gets the current gesture key map from the database."""
        if self.current_user_id is None:
            print("Предупреждение: get_current_gesture_key_map вызван до установки current_user_id")
            return {}
        gesture_key_map = get_user_gesture_bindings(self.db_path, self.current_user_id)
        print(f"Загружены связывания из базы данных для пользователя {self.current_user_id}: {gesture_key_map}")
        return gesture_key_map

    def start_video_stream(self, gesture_key_map):
        """Starts the video stream with the given gesture key map."""
        print("Запуск видеопотока...")
        if self.video_processor is not None:
            self.stop_video_stream()  # Stop any existing stream
        self.video_processor = VideoProcessor(gesture_key_map=gesture_key_map)
        self.settings_widget.set_video_processor(self.video_processor)
        self.video_processor.frame_ready.connect(self.update_frame)
        self.video_processor.start()
        print(f"VideoProcessor запущен для пользователя {self.current_user_id} с gesture_key_map: {gesture_key_map}")

    def stop_video_stream(self):
        """Stops the video stream."""
        print("Остановка видеопотока...")
        if self.video_processor is not None:
            self.video_processor.stop()
            self.video_processor.frame_ready.disconnect(self.update_frame)
            self.video_processor = None
            self.settings_widget.set_video_processor(None)
            print("VideoProcessor остановлен.")

    def update_frame(self, frame):
        if self.video_processor is not None and self.ui.functions_widget.currentWidget() == self.video_widget:  # Проверяем, что video_processor создан
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            self.video_widget.video_label.setPixmap(
                pixmap.scaled(self.video_widget.video_label.size(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.stop_video_stream()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())