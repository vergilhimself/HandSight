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
        # Get the updated gesture key map
        gesture_key_map = self.main_window.get_current_gesture_key_map()  # Get from MainWindow
        print(f"Переход в виджет трансляции, получен gesture_key_map: {gesture_key_map}")

        # Stop the existing video stream if it's running
        self.main_window.stop_video_stream()

        # Start a new video stream with the updated gesture key map
        self.main_window.start_video_stream(gesture_key_map)

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