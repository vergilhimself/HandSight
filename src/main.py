import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from src.gui.content_window import Ui_main_window
from src.funcs.functions import VideoProcessor

from src.gui.video_widget import VideoWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.video_widget = VideoWidget()
        self.ui.functions_widget.addWidget(self.video_widget)
        self.ui.functions_widget.setCurrentWidget(self.video_widget)

        self.video_processor = VideoProcessor()
        self.video_processor.frame_ready.connect(self.update_frame)
        self.video_processor.start()

    def update_frame(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.video_widget.video_label.setPixmap(pixmap.scaled(self.video_widget.video_label.size(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.video_processor.stop()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())