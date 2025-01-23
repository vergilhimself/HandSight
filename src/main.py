# D:\Projects\HandSight\src\main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.gui.content_window import Ui_main_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # Здесь можно добавить логику для ваших кнопок,
        # например:
        # self.ui.pushButton.clicked.connect(self.some_function)

    # def some_function(self):
    #     print("Кнопка нажата!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())