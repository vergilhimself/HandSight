from PyQt5.QtWidgets import QWidget
from src.qt_designer_files.video_widget_base import Ui_video_widget
from src.qt_designer_files.settings_widget_base import Ui_settings_widget
from src.qt_designer_files.gestures_widget_base import Ui_gestures_widget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


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

class GesturesWidget(QWidget, Ui_gestures_widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)