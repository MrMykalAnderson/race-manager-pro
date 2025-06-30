from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QApplication, QMessageBox, QTabWidget, QWidget
from PySide6.QtGui import QAction
from render.qt.tab_manager import TabManager


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

        # Tab system
        self.tab_manager = TabManager(self)
        self.setCentralWidget(self.tab_manager)

        # Start with one blank tab
        from render.qt.blank_view_window import BlankViewWindow

    @classmethod
    def open_new_window(cls, window_class):
        window = window_class()
        window.show()
        cls._open_windows.append(window)

        def handle_close(event):
            cls._open_windows.remove(window)
            if not cls._open_windows:
                QApplication.instance().quit()
            super(window_class, window).closeEvent(event)

        window.closeEvent = handle_close

    def switch_view(self, new_view_class):
        new_tab = new_view_class()
        self.tab_manager.add_tab(new_tab)
