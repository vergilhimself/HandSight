from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGraphicsBlurEffect, \
    QListWidget, QListWidgetItem, QHBoxLayout, QFrame, QInputDialog, QKeySequenceEdit, QDialog
from PyQt5.QtGui import QKeySequence, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
from qt_designer_files.gestures_widget_base import Ui_gestures_widget
from qt_designer_files.login_widget_base import Ui_login_widget
from qt_designer_files.video_widget_base import Ui_video_widget
from qt_designer_files.settings_widget_base import Ui_settings_widget
# import для db
from funcs.db_funcs import hash_password, get_user, create_user, get_user_gesture_bindings, save_user_gesture_binding
import os
import pyautogui
import sqlite3
from funcs.video_processor import VideoProcessor
from funcs.command_funcs import load_standard_gestures, parse_key_sequence


class VideoWidget(QWidget, Ui_video_widget):
    def __init__(self, parent=None, video_processor=None):
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
        if self.video_processor is not None:  # Если есть текущий VideoProcessor
            print(
                f"SettingsWidget.save_settings: Применение настроек к текущему VideoProcessor (ID: {id(self.video_processor)})")
            self.video_processor.cap_device = self.device_spinbox.value()
            self.video_processor.cap_width = self.width_spinbox.value()
            self.video_processor.cap_height = self.height_spinbox.value()
            self.video_processor.use_static_image_mode = self.use_static_image_mode_checkbox.isChecked()
            self.video_processor.min_detection_confidence = self.min_detection_confidence_doublespinbox.value()
            self.video_processor.min_tracking_confidence = self.min_tracking_confidence_doublespinbox.value()
            self.video_processor.use_brect = self.use_brect_checkbox.isChecked()

            print(
                f"SettingsWidget: Параметры обновлены для текущего VP. MinDetectConf: {self.video_processor.min_detection_confidence}")

            if self.video_processor.running:  # Если поток запущен, перезапускаем его для применения
                print("SettingsWidget: Текущий поток запущен, перезапускаем его для применения настроек...")
                self.video_processor.stop()
                # start() вызовет _run, который использует обновленные атрибуты
                try:
                    self.video_processor.start()

                except Exception as e:
                    print()("Ошибка", f"Не удалось перезапустить видеопоток: {e}")
            else:
                print("Настройки обновлены",
                                        "Настройки обновлены. Они применятся при следующем запуске трансляции.")
        else:
            print("SettingsWidget: video_processor не установлен (None), настройки не применены к потоку.")


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
        user_id = get_user(self.db_path, login, password)
        if user_id:
            self.close_login()
            self.main_window.set_current_user(user_id)
            QMessageBox.information(self, "Успех", f"Вы успешно вошли как {login}")
        else:
            self.error_label.setText("Неправильный логин или пароль")

    def register(self):
        login = self.login_line_edit.text()
        password = self.password_line_edit.text()
        if create_user(self.db_path, login, password):
            QMessageBox.information(self, "Успех", f"Пользователь {login} успешно зарегистрирован")
            user_id = get_user(self.db_path, login, password)
            self.main_window.set_current_user(user_id)
            self.close_login()
        else:
            self.error_label.setText("Пользователь с таким логином уже существует")


class KeyPressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Нажмите клавишу или кнопку мыши")
        self.layout = QVBoxLayout()
        self.label = QLabel("Ожидание нажатия клавиши...")
        self.layout.addWidget(self.label)
        self.key_sequence = "" # Строка для хранения последовательности нажатий
        self.setLayout(self.layout)
        self.setModal(True) # Блокируем родительское окно
        self.result = None #  Переменная для хранения результата (клавиша/кнопка)

    def keyPressEvent(self, event):
        # Обработка нажатия клавиш
        key = event.key()
        modifiers = event.modifiers()

        key_text = ""

        if modifiers & Qt.ControlModifier:
            key_text += "Ctrl+"
        if modifiers & Qt.ShiftModifier:
            key_text += "Shift+"
        if modifiers & Qt.AltModifier:
            key_text += "Alt+"

        key_text += event.text() if event.text() else Qt.Key(key).name # Получаем имя клавиши

        self.result = key_text
        self.accept() # Закрываем диалог и возвращаем результат

    def mousePressEvent(self, event):
        # Обработка нажатий мыши
        button = event.button()
        button_text = ""
        if button == Qt.LeftButton:
            button_text = "Левая кнопка мыши"
        elif button == Qt.RightButton:
            button_text = "Правая кнопка мыши"
        elif button == Qt.MiddleButton:
            button_text = "Средняя кнопка мыши"
        else:
            button_text = "Другая кнопка мыши"

        self.result = button_text
        self.accept()  # Закрываем диалог и возвращаем результат


    def get_key_sequence(self):
        return self.result # Возвращаем строку с клавишей/кнопкой

class GesturesWidget(QWidget, Ui_gestures_widget):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.setupUi(self)
        self.current_user = current_user
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "handsight.db")
        print(f"Путь к базе данных: {self.db_path}")
        self.user_id = self.get_user_id_from_login(self.db_path, current_user)
        print(f"User ID: {self.user_id}")
        self.standard_gestures = load_standard_gestures()
        print(f"Стандартные жесты: {self.standard_gestures}")
        self.display_gestures()

        self.gesture_key_map = self.load_gesture_key_map()  # Загружаем словарь
        print(f"Загруженные связки: {self.gesture_key_map}")

        # Словарь для хранения связей жест -> клавиша/кнопка
        self.gesture_keys = {}
        # Подключаем сигнал itemClicked к функции для отображения диалога назначения клавиши
        self.gesture_list.itemClicked.connect(self.show_key_press_dialog)

    def load_gesture_key_map(self):
        """Загружает и возвращает словарь привязок."""
        return get_user_gesture_bindings(self.db_path, self.user_id)

    def get_user_id_from_login(self, db_path, login):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Users WHERE id = ?", (login,))
            user = cursor.fetchone()
            conn.close()
            return user[0] if user else None
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса get_user: {e}")
            return None

    def display_gestures(self):
        print(f"Gestures List Widget: {self.gesture_list}")
        if self.standard_gestures:
            for gesture in self.standard_gestures:
                self.gesture_list.addItem(f"{gesture['name']}")
        else:
            self.gesture_list.addItem("Нет доступных жестов.")

    def show_key_press_dialog(self, item):
        gesture_name = item.text()  # Получаем текст выбранного элемента (имя жеста)

        dialog = KeyPressDialog(self) # Создаем диалог
        result = dialog.exec_() # Открываем диалог

        if result == QDialog.Accepted: # Если клавиша/кнопка нажата
            key_sequence = dialog.get_key_sequence() # Получаем последовательность
            self.gesture_keys[gesture_name] = key_sequence  # Сохраняем связь жест -> клавиша
            print(f"Клавиша/кнопка '{key_sequence}' назначена для жеста '{gesture_name}'") # Отладочный вывод
            print(f"Текущие связи: {self.gesture_keys}") # Отладочный вывод
            save_user_gesture_binding(self.db_path, self.user_id, gesture_name, key_sequence)
        else:
            print("Диалог отменен")