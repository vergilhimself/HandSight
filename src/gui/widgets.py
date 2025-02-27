from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGraphicsBlurEffect, \
    QListWidget, QListWidgetItem, QHBoxLayout, QFrame, QInputDialog, QKeySequenceEdit
from PyQt5.QtGui import QKeySequence, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt
from qt_designer_files.gestures_widget_base import Ui_gestures_widget
from qt_designer_files.login_widget_base import Ui_login_widget
from qt_designer_files.video_widget_base import Ui_video_widget
from qt_designer_files.settings_widget_base import Ui_settings_widget
# import для db
from funcs.db_funcs import get_user_gestures, update_keyboard_shortcut, remove_user_gesture, get_user, create_user, \
    hash_password, add_new_custom_gesture
import os
import sqlite3
import json
from funcs.video_processor import VideoProcessor

def load_standard_gestures():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "..", "data", "standard_gestures.json")
        with open(file_path, "r", encoding="utf-8") as f:
            standard_gestures = json.load(f)
        return standard_gestures
    except FileNotFoundError:
        QMessageBox.critical(None, "Ошибка", "Файл standard_gestures.json не найден!")
        return []
    except json.JSONDecodeError:
        QMessageBox.critical(None, "Ошибка", "Ошибка при чтении standard_gestures.json!")
        return []


class VideoWidget(QWidget, Ui_video_widget):
    def __init__(self, parent=None, video_processor = None):
        super().__init__(parent)
        self.setupUi(self)
        self.video_processor = video_processor

    def set_mode(self, mode):
        if self.video_processor:
            self.video_processor.mode = mode
            print(f"Режим изменен на: {mode}")
        else:
            print("video_processor не установлен")

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
        self.video_processor = VideoProcessor()
        self.load_settings()

        self.device_spinbox.valueChanged.connect(self.save_settings)
        self.width_spinbox.valueChanged.connect(self.save_settings)
        self.height_spinbox.valueChanged.connect(self.save_settings)
        self.use_static_image_mode_checkbox.stateChanged.connect(self.save_settings)
        self.min_detection_confidence_doublespinbox.valueChanged.connect(self.save_settings)
        self.min_tracking_confidence_doublespinbox.valueChanged.connect(self.save_settings)
        self.use_brect_checkbox.stateChanged.connect(self.save_settings)

    def set_video_processor(self, video_processor):
        self.video_processor = video_processor
        self.load_settings()

    def load_settings(self):
        if self.video_processor:
            self.device_spinbox.setValue(self.video_processor.cap_device)
            self.width_spinbox.setValue(self.video_processor.cap_width)
            self.height_spinbox.setValue(self.video_processor.cap_height)
            self.use_static_image_mode_checkbox.setChecked(self.video_processor.use_static_image_mode)
            self.min_detection_confidence_doublespinbox.setValue(self.video_processor.min_detection_confidence)
            self.min_tracking_confidence_doublespinbox.setValue(self.video_processor.min_tracking_confidence)
            self.use_brect_checkbox.setChecked(self.video_processor.use_brect)

    def save_settings(self):
        if self.video_processor:
            self.video_processor.cap_device = self.device_spinbox.value()
            self.video_processor.cap_width = self.width_spinbox.value()
            self.video_processor.cap_height = self.height_spinbox.value()
            self.video_processor.use_static_image_mode = self.use_static_image_mode_checkbox.isChecked()
            self.video_processor.min_detection_confidence = self.min_detection_confidence_doublespinbox.value()
            self.video_processor.min_tracking_confidence = self.min_tracking_confidence_doublespinbox.value()
            self.video_processor.use_brect = self.use_brect_checkbox.isChecked()

            self.video_processor.stop()
            self.video_processor.start()


class LoginWidget(QWidget, Ui_login_widget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        # Использование относительного пути
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "handsight.db")
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        self.error_label.setText("")

        self.setVisible(False)

    def show_login(self):
        self.setVisible(True)

    def close_login(self):
        self.setVisible(False)

    def login(self):
        login = self.login_line_edit.text()
        password = self.password_line_edit.text()
        hashed_password = hash_password(password)

        if not login or not password:
            self.error_label.setText("Заполните все поля")
            return

        user_id = get_user(self.db_path, login, hashed_password)
        if user_id:
            self.close_login()
            self.main_window.set_current_user(login)
            QMessageBox.information(self, "Успех", f"Вы успешно вошли как {login}")
        else:
            self.error_label.setText("Неправильный логин или пароль")

    def register(self):
        login = self.login_line_edit.text()
        password = self.password_line_edit.text()
        hashed_password = hash_password(password)

        if not login or not password:
            self.error_label.setText("Заполните все поля")
            return

        if create_user(self.db_path, login, hashed_password):
            self.close_login()
            self.main_window.set_current_user(login)
            QMessageBox.information(self, "Успех", f"Пользователь {login} успешно зарегистрирован")
        else:
            self.error_label.setText("Пользователь с таким логином уже существует")


class GestureItemWidget(QWidget):
    def __init__(self, gesture, parent=None):
        super().__init__(parent)

        # Основной layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)  # Отступы

        # Устанавливаем стиль для фона элемента
        self.setStyleSheet("""
            GestureItemWidget {
                background-color: #3e414a;
                border-radius: 10px; /* Закругление углов */
                color: white; /* Белый цвет шрифта */
            }
        """)
        # Имя жеста
        self.name_label = QLabel(gesture["name"])
        font = QFont("Comic Sans MS", 12)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet("color: white;")
        layout.addWidget(self.name_label)

        # Создаем QLineEdit для редактирования имени жеста
        self.edit_name_line = QLineEdit()
        self.edit_name_line.setText(gesture["name"])

        # Добавляем QKeySequenceEdit
        self.key_sequence_edit = QKeySequenceEdit()
        layout.addWidget(self.key_sequence_edit)

        # Добавляем кнопку "Удалить"
        self.delete_button = QPushButton("Удалить")
        layout.addWidget(self.delete_button)

        # Добавляем виджеты в layout
        layout.addWidget(self.name_label)


class GesturesWidget(QWidget, Ui_gestures_widget):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.setupUi(self)
        self.current_user = current_user
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "handsight.db")
        self.user_id = self.get_user_id_from_login(self.db_path, current_user)  # Получаем user_id
        self.standard_gestures = load_standard_gestures()
        self.gestures = []  # список жестов
        self.load_gestures()  # загружаем жесты
        self.add_gesture_button.clicked.connect(self.add_new_gesture)
        self.update_gesture_list()  # обновляем список жестов

    def get_user_id_from_login(self, db_path, login):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Users WHERE login = ?", (login,))
            user = cursor.fetchone()
            conn.close()
            return user[0] if user else None  # Возвращаем id пользователя, если найден, иначе None
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса get_user: {e}")
            return None

    def load_gestures(self):
        if self.user_id:
            user_gestures = get_user_gestures(self.db_path, self.user_id)
            self.gestures = self.standard_gestures + user_gestures
            # self.gestures.sort(key = lambda x: x["is_standard"], reverse = True) # Сначала стандартные

    def update_gesture_list(self):
        self.gesture_list.clear()
        for gesture in self.gestures:
            self.add_gesture_to_list(gesture)

    def add_gesture_to_list(self, gesture):
        item = QListWidgetItem()
        item_widget = GestureItemWidget(gesture)  # Use the custom widget

        # Set size hint and add widget to item
        item.setSizeHint(item_widget.sizeHint())
        self.gesture_list.addItem(item)
        self.gesture_list.setItemWidget(item, item_widget)

    def delete_gesture(self, gesture):
        # todo реализовать удаление
        pass

    def change_name_gesture(self, gesture):
        # todo реализовать изменение имени
        pass

    def change_bind_gesture(self, gesture):
        # todo реализовать изменение бинда
        pass

    def add_new_gesture(self):
        # todo реализовать добавление
        pass
