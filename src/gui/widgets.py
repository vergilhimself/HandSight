import os
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QRadioButton, QButtonGroup, QHBoxLayout, \
    QMessageBox, QSpacerItem, QSizePolicy, QComboBox
from funcs.command_funcs import load_standard_gestures, parse_key_sequence
# import для db
from funcs.db_funcs import hash_password, get_user, create_user, get_user_gesture_bindings, save_user_gesture_binding
from funcs.video_processor import VideoProcessor
from qt_designer_files.gestures_widget_base import Ui_gestures_widget
from qt_designer_files.login_widget_base import Ui_login_widget
from qt_designer_files.settings_widget_base import Ui_settings_widget
from qt_designer_files.video_widget_base import Ui_video_widget


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
        if self.video_processor is not None:
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
                f'SettingsWidget: Параметры обновлены для текущего VP. MinDetectConf: {self.video_processor
                                                                                    .min_detection_confidence}')

            if self.video_processor.running:
                print("SettingsWidget: Текущий поток запущен, перезапускаем его для применения настроек...")
                self.video_processor.stop()

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

        self.gesture_key_map = self.load_gesture_key_map()
        print(f"Загруженные связки: {self.gesture_key_map}")

        # Словарь для хранения связей жест -> клавиша/кнопка
        self.gesture_keys = {}
        # Подключаем сигнал itemClicked к функции для отображения диалога назначения клавиши
        self.gesture_list.itemClicked.connect(self.show_key_press_dialog)

    def load_gesture_key_map(self):
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
        print("--- GesturesWidget.show_key_press_dialog CALLED ---")
        try:
            if item is None:
                print("ERROR: 'item' is None in show_key_press_dialog!")
                return

            gesture_name = item.text()
            print(f"Attempting to show dialog for gesture: '{gesture_name}'")
            print(f"Current user_id: {self.user_id}")

            if self.user_id is None:
                print("ERROR: self.user_id is None. Cannot proceed.")
                QMessageBox.warning(self, "Ошибка", "ID пользователя не определен. Невозможно назначить привязку.")
                return

            print("Creating AssignBindingDialog...")
            dialog = AssignBindingDialog(gesture_name, self)
            print(f"AssignBindingDialog created. Parent: {dialog.parent()}")

            print("Executing dialog.exec_()...")
            result_code = dialog.exec_()
            print(f"dialog.exec_() finished with result_code: {result_code}")

            if result_code == QDialog.Accepted:
                key_sequence_str_for_db = dialog.get_key_sequence_for_db()
                print(f"Dialog accepted. key_sequence_str_for_db: '{key_sequence_str_for_db}'")

                if key_sequence_str_for_db:
                    print(f"Для жеста '{gesture_name}' назначено: '{key_sequence_str_for_db}'")
                    self.gesture_keys[gesture_name] = key_sequence_str_for_db

                    save_user_gesture_binding(
                        db_path=self.db_path,
                        user_id=self.user_id,
                        gesture_name=gesture_name,
                        key_sequence=key_sequence_str_for_db
                    )
                    print(
                        "GesturesWidget: Привязка сохранена. Изменения вступят в силу при следующем запуске/перезапуске трансляции.")
                    QMessageBox.information(self, "Привязка сохранена",
                                            "Новая привязка жеста сохранена.\n"
                                            "Она будет активна при следующем запуске трансляции.")
                else:
                    print(f"Диалог для жеста '{gesture_name}' принят, но строка для БД пустая.")
            else:
                print(f"Диалог назначения для жеста '{gesture_name}' отменен или закрыт.")

        except Exception as e:
            print(f"CRITICAL ERROR in GesturesWidget.show_key_press_dialog: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Критическая ошибка",
                                 f"Произошла ошибка при открытии диалога назначения: {e}")


class AssignBindingDialog(QDialog):
    def __init__(self, gesture_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Назначить действие для '{gesture_name}'")
        self.setMinimumWidth(350)

        self.layout = QVBoxLayout(self)

        self.action_type_group = QButtonGroup(self)
        self.keyboard_radio = QRadioButton("Клавиатурное сокращение", self)
        self.mouse_radio = QRadioButton("Действие мыши", self)
        self.action_type_group.addButton(self.keyboard_radio)
        self.action_type_group.addButton(self.mouse_radio)

        type_layout = QHBoxLayout()
        type_layout.addWidget(self.keyboard_radio)
        type_layout.addWidget(self.mouse_radio)
        self.layout.addLayout(type_layout)

        self.keyboard_group_label = QLabel("Выберите клавиши:", self)
        self.layout.addWidget(self.keyboard_group_label)

        self.modifiers_combo = QComboBox(self)
        self.modifiers_combo.addItem("Нет модификаторов", Qt.NoModifier)
        self.modifiers_combo.addItem("Ctrl", Qt.ControlModifier)
        self.modifiers_combo.addItem("Shift", Qt.ShiftModifier)
        self.modifiers_combo.addItem("Alt", Qt.AltModifier)
        self.modifiers_combo.addItem("Ctrl + Shift", Qt.ControlModifier | Qt.ShiftModifier)
        self.modifiers_combo.addItem("Ctrl + Alt", Qt.ControlModifier | Qt.AltModifier)
        self.modifiers_combo.addItem("Shift + Alt", Qt.ShiftModifier | Qt.AltModifier)
        self.modifiers_combo.addItem("Ctrl + Shift + Alt", Qt.ControlModifier | Qt.ShiftModifier | Qt.AltModifier)
        self.layout.addWidget(self.modifiers_combo)

        self.key_combo = QComboBox(self)
        for i in range(ord('A'), ord('Z') + 1): self.key_combo.addItem(chr(i), Qt.Key(i))
        for i in range(ord('0'), ord('9') + 1): self.key_combo.addItem(chr(i), Qt.Key(i))
        self.key_combo.addItem("Space", Qt.Key_Space)
        self.key_combo.addItem("Enter", Qt.Key_Return)
        self.key_combo.addItem("Escape", Qt.Key_Escape)
        self.key_combo.addItem("Tab", Qt.Key_Tab)
        for i in range(1, 13): self.key_combo.addItem(f"F{i}", getattr(Qt, f"Key_F{i}"))
        self.layout.addWidget(self.key_combo)

        self.mouse_group_label = QLabel("Выберите кнопку мыши:", self)
        self.layout.addWidget(self.mouse_group_label)

        self.mouse_button_combo = QComboBox(self)
        self.mouse_button_combo.addItem("Левая кнопка мыши", Qt.LeftButton)
        self.mouse_button_combo.addItem("Правая кнопка мыши", Qt.RightButton)
        self.mouse_button_combo.addItem("Средняя кнопка мыши", Qt.MiddleButton)
        self.layout.addWidget(self.mouse_button_combo)

        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.button_box_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.custom_accept)
        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_box_layout.addStretch()
        self.button_box_layout.addWidget(self.ok_button)
        self.button_box_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_box_layout)

        self.keyboard_radio.toggled.connect(self.toggle_sections)
        self.mouse_radio.toggled.connect(self.toggle_sections)
        self.keyboard_radio.setChecked(True)
        self.toggle_sections()

        self.setModal(True)
        self.result_key_sequence_for_db = None

    def toggle_sections(self):
        is_keyboard = self.keyboard_radio.isChecked()
        self.keyboard_group_label.setVisible(is_keyboard)
        self.modifiers_combo.setVisible(is_keyboard)
        self.key_combo.setVisible(is_keyboard)
        self.mouse_group_label.setVisible(not is_keyboard)
        self.mouse_button_combo.setVisible(not is_keyboard)

    def custom_accept(self):
        if self.keyboard_radio.isChecked():
            modifier_data = self.modifiers_combo.currentData()
            key_data = self.key_combo.currentData()

            if key_data is None:
                QMessageBox.warning(self, "Ошибка", "Основная клавиша не выбрана.")
                return

            text_parts = []
            if modifier_data != Qt.NoModifier:
                if modifier_data & Qt.ControlModifier: text_parts.append("Ctrl")
                if modifier_data & Qt.ShiftModifier: text_parts.append("Shift")
                if modifier_data & Qt.AltModifier: text_parts.append("Alt")
            text_parts.append(self.key_combo.currentText())

            self.result_key_sequence_for_db = " + ".join(text_parts)
            print(f"AssignBindingDialog: Keyboard selected. Result for DB: '{self.result_key_sequence_for_db}'")

        elif self.mouse_radio.isChecked():
            self.result_key_sequence_for_db = self.mouse_button_combo.currentText()
            print(f"AssignBindingDialog: Mouse selected. Result for DB: '{self.result_key_sequence_for_db}'")
        else:
            QMessageBox.warning(self, "Ошибка", "Не выбран тип действия (клавиатура или мышь).")
            return
        print(
            f"AssignBindingDialog: Keyboard selected. Result for DB: '{self.result_key_sequence_for_db}'")
        super().accept()

    def get_key_sequence_for_db(self):
        return self.result_key_sequence_for_db
