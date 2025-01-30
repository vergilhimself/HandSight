from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsBlurEffect, \
    QListWidget, QListWidgetItem, QHBoxLayout, QFrame, QInputDialog
from src.qt_designer_files.login_widget_base import Ui_login_widget
from src.qt_designer_files.video_widget_base import Ui_video_widget
from src.qt_designer_files.settings_widget_base import Ui_settings_widget
from src.qt_designer_files.gestures_widget_base import Ui_gestures_widget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import os
from src.funcs.db_funcs import hash_password, get_user, create_user, get_user_gestures, save_user_gestures


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
        self.video_processor = None
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


from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGraphicsBlurEffect
from src.qt_designer_files.login_widget_base import Ui_login_widget
import sqlite3
import hashlib
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from src.funcs.db_funcs import hash_password, get_user, create_user, get_user_gestures, save_user_gestures


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

        self.blur_effect = QGraphicsBlurEffect(self.blur_widget)  # Создаем blur effect
        self.blur_effect.setBlurRadius(30)  # Устанавливаем радиус размытия
        self.blur_widget.setStyleSheet(
            "background-color: rgba(217, 217, 217, 0.7);")  # устанавливаем полупрозрачный фон для blur_widget
        self.setVisible(False)
        self.message_timer = QTimer(self)
        self.message_timer.timeout.connect(self.clear_message)

    def show_login(self):
        self.setVisible(True)

    def close_login(self):
        self.setVisible(False)

    def login(self):
        login = self.login_line_edit.text()
        password = self.password_line_edit.text()
        hashed_password = hash_password(password)

        if not login or not password:
            self.show_message("Заполните все поля")
            return

        user = get_user(self.db_path, login, hashed_password)
        if user:
            self.close_login()
            self.main_window.set_current_user(login)
            self.show_message(f"Вы успешно вошли как {login}")
        else:
            self.show_message("Неправильный логин или пароль")

    def register(self):
        login = self.login_line_edit.text()
        password = self.password_line_edit.text()
        hashed_password = hash_password(password)

        if not login or not password:
            self.show_message("Заполните все поля")
            return

        if create_user(self.db_path, login, hashed_password):
            self.close_login()
            self.main_window.set_current_user(login)
            self.show_message(f"Пользователь {login} успешно зарегистрирован")
        else:
            self.show_message("Пользователь с таким логином уже существует")

    def show_message(self, message):
        self.error_label.setText(message)
        self.message_timer.start(3000)  # сообщение исчезнет через 3 секунды

    def clear_message(self):
        self.error_label.setText("")
        self.message_timer.stop()


class GesturesWidget(QWidget, Ui_gestures_widget):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "handsight.db")
        self.gestures = []
        self.current_user = current_user
        self.load_gestures()
        self.add_gesture_button.clicked.connect(self.add_new_gesture)

    def load_gestures(self):
        if self.current_user:
            self.gestures = get_user_gestures(self.db_path, self.current_user)
        self.update_gesture_list()

    def save_gestures(self):
        if self.current_user:
            save_user_gestures(self.db_path, self.current_user, self.gestures)

    def update_gesture_list(self):
        self.gesture_list.clear()
        for gesture in self.gestures:
            self.add_gesture_to_list(gesture)

    def add_gesture_to_list(self, gesture):
        item = QListWidgetItem()
        item_widget = self.create_gesture_item_widget(gesture)
        item.setSizeHint(item_widget.sizeHint())
        self.gesture_list.addItem(item)
        self.gesture_list.setItemWidget(item, item_widget)

    def create_gesture_item_widget(self, gesture):
        item_widget = QFrame()
        layout = QHBoxLayout()
        item_widget.setLayout(layout)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(lambda: self.delete_gesture(gesture))
        rename_button = QPushButton("Переименовать")
        rename_button.clicked.connect(lambda: self.rename_gesture(gesture))

        layout.addWidget(QPushButton(gesture["name"]))
        layout.addWidget(delete_button)
        layout.addWidget(rename_button)

        return item_widget

    def delete_gesture(self, gesture):
        self.gestures.remove(gesture)
        self.save_gestures()
        self.update_gesture_list()

    def rename_gesture(self, gesture):
        new_name, ok = QInputDialog.getText(self, "Переименовать жест", "Новое имя:", text=gesture['name'])
        if ok and new_name:
            gesture["name"] = new_name
            self.save_gestures()
            self.update_gesture_list()

    def add_new_gesture(self):
        new_gesture_name, ok = QInputDialog.getText(self, "Новый жест", "Имя нового жеста:")

        if ok and new_gesture_name:
            new_gesture = {"name": new_gesture_name, "data": "new_gesture_data"}
            self.gestures.append(new_gesture)
            self.save_gestures()
            self.add_gesture_to_list(new_gesture)