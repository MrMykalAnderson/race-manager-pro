from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QApplication, QMessageBox
from PySide6.QtGui import QAction
import sys


class BaseWindow(QMainWindow):
    _open_windows = []  # Tracks all open windows

    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Race Manager Pro")

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # File Menu
        file_menu = QMenu("File", self)
        self.menu_bar.addMenu(file_menu)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    @classmethod
    def open_new_window(cls, window_class):
        window = window_class()
        window.show()
        cls._open_windows.append(window)

        # Ensure window is removed on close
        def handle_close(event):
            cls._open_windows.remove(window)
            if not cls._open_windows:
                QApplication.instance().quit()
            super(window_class, window).closeEvent(event)

        window.closeEvent = handle_close