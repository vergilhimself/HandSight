class NavigationManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def show_video_widget(self):
        self.main_window.ui.functions_widget.setCurrentWidget(self.main_window.video_widget)

    def show_settings_widget(self):
        self.main_window.ui.functions_widget.setCurrentWidget(self.main_window.settings_widget)