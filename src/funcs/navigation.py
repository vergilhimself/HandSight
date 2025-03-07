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
