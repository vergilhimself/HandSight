import mediapipe as mp
import sys
import sqlite3
import os  # Импортируем модуль os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from gui.content_window import Ui_main_window
from funcs.video_processor import VideoProcessor
from gui.widgets import VideoWidget, SettingsWidget, GesturesWidget, LoginWidget
from funcs.navigation import NavigationManager
from src.funcs.db_funcs import get_user_gesture_bindings, create_user_gesture_bindings_table

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

    def start_video_stream(self, gesture_key_map, cap_device, cap_width, cap_height,
                           use_static_image_mode, min_detection_confidence, min_tracking_confidence, use_brect):
        """
        Starts or restarts the video stream with specified parameters and gesture key map.
        """
        print("Запуск/перезапуск видеопотока с новыми параметрами...")

        if self.video_processor is not None:
            print(f"Остановка существующего VideoProcessor (ID: {id(self.video_processor)}) перед перезапуском.")
            self.video_processor.stop() # Останавливаем предыдущий, если был
            try:
                self.video_processor.frame_ready.disconnect(self.update_frame)
            except TypeError:
                pass # Уже был отсоединен или не подключен

        # Создаем НОВЫЙ экземпляр VideoProcessor с переданными параметрами
        print(f"Создание нового VideoProcessor с параметрами: device={cap_device}, width={cap_width}, height={cap_height}, "
              f"static_mode={use_static_image_mode}, min_detect_conf={min_detection_confidence}, "
              f"min_track_conf={min_tracking_confidence}, use_brect={use_brect}")
        self.video_processor = VideoProcessor(
            device=cap_device,
            width=cap_width,
            height=cap_height,
            use_static_image_mode=use_static_image_mode,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            gesture_key_map=gesture_key_map
        )
        # self.video_processor.use_brect можно установить отдельно, если его нет в конструкторе VideoProcessor
        # или если конструктор VideoProcessor не принимает все эти параметры, их нужно установить в атрибуты после создания.
        # В вашем VideoProcessor конструктор принимает большинство этих параметров.
        # Убедимся, что use_brect также устанавливается, если VideoProcessor.__init__ его не устанавливает.
        # В вашем коде VideoProcessor.__init__ устанавливает self.use_brect = True по умолчанию,
        # так что если вы хотите передавать его, измените VideoProcessor.__init__ или установите здесь:
        self.video_processor.use_brect = use_brect # Устанавливаем, если нужно

        # ВАЖНО: SettingsWidget теперь должен быть уведомлен о НОВОМ экземпляре video_processor
        # чтобы его UI отображал актуальные значения (хотя при таком подходе он их и так не хранит)
        # и чтобы он мог сохранить их в этот новый экземпляр, если бы его save_settings вызывался.
        # Для простоты можно считать, что SettingsWidget всегда читает из video_processor.
        self.settings_widget.set_video_processor(self.video_processor)
        # И VideoWidget тоже
        if hasattr(self.video_widget, 'video_processor'):
             self.video_widget.video_processor = self.video_processor
        elif hasattr(self.video_widget, 'set_video_processor'):
             self.video_widget.set_video_processor(self.video_processor)


        self.video_processor.frame_ready.connect(self.update_frame)
        try:
            self.video_processor.start()
            print(f"Новый VideoProcessor (ID: {id(self.video_processor)}) запущен с gesture_key_map: {gesture_key_map}")
        except Exception as e:
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"ERROR starting NEW VideoProcessor: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка запуска", f"Не удалось запустить видеопоток: {e}")
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def stop_video_stream(self):
        print("Остановка видеопотока...")
        if self.video_processor is not None:
            print(f"Останавливаем VideoProcessor (ID: {id(self.video_processor)})")
            self.video_processor.stop()
            try:
                self.video_processor.frame_ready.disconnect(self.update_frame)
            except TypeError:
                pass
            # При таком подходе можно обнулять video_processor, так как он всегда пересоздается
            # self.video_processor = None
            # self.settings_widget.set_video_processor(None) # И сбрасывать в виджетах
            # Но если мы хотим, чтобы SettingsWidget отображал последние активные настройки,
            # то лучше не обнулять, а просто останавливать. Решите, какая семантика нужна.
            # Пока оставим его не None для согласованности с выводом лога.
        else:
            print("VideoProcessor не существует (равен None) или уже остановлен.")

    def update_frame(self, frame):
        if self.video_processor is not None and self.ui.functions_widget.currentWidget() == self.video_widget:  # Проверяем, что video_processor создан
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            self.video_widget.video_label.setPixmap(
                pixmap.scaled(self.video_widget.video_label.size(), Qt.KeepAspectRatio))

    def is_video_widget_active(self):
        """Checks if the video widget is the current widget."""
        return self.ui.functions_widget.currentWidget() == self.video_widget

    def closeEvent(self, event):
        self.stop_video_stream()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())