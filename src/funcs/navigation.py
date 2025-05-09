import sys
from PyQt5.QtWidgets import QApplication


class NavigationManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.gestures_widget = None
        self.current_user = None

    def set_current_user(self, current_user):
        self.current_user = current_user

    def show_video_widget(self):
        print("NavigationManager: Переход в виджет трансляции и запуск/перезапуск потока.")
        gesture_key_map = self.main_window.get_current_gesture_key_map()

        # --- Получаем параметры из SettingsWidget ---
        # Это предполагает, что self.main_window.settings_widget уже существует и инициализирован
        # и его UI-элементы (spinbox, checkbox) доступны.
        # Также SettingsWidget должен иметь video_processor, из которого можно было бы читать,
        # но если мы всегда пересоздаем, то читаем прямо из UI SettingsWidget.
        # Важно: SettingsWidget должен быть инициализирован и его UI доступен.
        sw = self.main_window.settings_widget
        if sw.video_processor is None: # Если VideoProcessor в SettingsWidget еще не был установлен (первый запуск)
                                     # используем дефолтные значения или значения из UI по умолчанию.
            print("NavigationManager: video_processor в SettingsWidget еще не установлен. Используем значения из UI SettingsWidget.")
            cap_device = sw.device_spinbox.value()
            cap_width = sw.width_spinbox.value()
            cap_height = sw.height_spinbox.value()
            use_static_image_mode = sw.use_static_image_mode_checkbox.isChecked()
            min_detection_confidence = sw.min_detection_confidence_doublespinbox.value()
            min_tracking_confidence = sw.min_tracking_confidence_doublespinbox.value()
            use_brect = sw.use_brect_checkbox.isChecked()
        else: # Читаем текущие значения из video_processor, который привязан к SettingsWidget.
              # Это полезно, если video_processor не None и SettingsWidget отражает его состояние.
              # Но поскольку мы всегда пересоздаем VP, можно всегда читать из UI SettingsWidget.
              # Для простоты и консистентности с "всегда пересоздаем", читаем из UI.
            print("NavigationManager: Чтение параметров напрямую из UI SettingsWidget.")
            cap_device = sw.device_spinbox.value()
            cap_width = sw.width_spinbox.value()
            cap_height = sw.height_spinbox.value()
            use_static_image_mode = sw.use_static_image_mode_checkbox.isChecked()
            min_detection_confidence = sw.min_detection_confidence_doublespinbox.value()
            min_tracking_confidence = sw.min_tracking_confidence_doublespinbox.value()
            use_brect = sw.use_brect_checkbox.isChecked()


        # Вызываем метод MainWindow для запуска/перезапуска потока с этими параметрами
        self.main_window.start_video_stream(
            gesture_key_map,
            cap_device,
            cap_width,
            cap_height,
            use_static_image_mode,
            min_detection_confidence,
            min_tracking_confidence,
            use_brect
        )

        # Показываем виджет видео
        self.main_window.ui.functions_widget.setCurrentWidget(self.main_window.video_widget)

    def show_settings_widget(self):
        self.main_window.ui.functions_widget.setCurrentWidget(self.main_window.settings_widget)

    def show_gestures_widget(self):
        if not self.gestures_widget:
            from src.gui.widgets import GesturesWidget
            self.gestures_widget = GesturesWidget(self.main_window, self.current_user)
            self.main_window.ui.functions_widget.addWidget(self.gestures_widget)
        self.main_window.ui.functions_widget.setCurrentWidget(self.gestures_widget)

    def exit_app(self):
        self.main_window.close()