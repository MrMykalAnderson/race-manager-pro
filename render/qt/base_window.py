from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QApplication, QMessageBox
from PySide6.QtGui import QAction
from render.qt.track_editor_window import TrackEditorWindow
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

        # Add New Window action
        new_window_action = QAction("New Window", self)
        new_window_action.triggered.connect(lambda: BaseWindow.open_new_window(BlankViewWindow))
        file_menu.addAction(new_window_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)


        # View Menu
        view_menu = QMenu("View", self)
        self.menu_bar.addMenu(view_menu)

        from render.qt.track_editor_window import TrackEditorWindow  # near top of file

        # Switch to Blank View
        blank_view_action = QAction("Blank View", self)
        from render.qt.blank_view_window import BlankViewWindow
        blank_view_action.triggered.connect(lambda: self.switch_view(BlankViewWindow))
        view_menu.addAction(blank_view_action)

        # Switch to Track Editor
        track_editor_action = QAction("Track Editor", self)
        track_editor_action.triggered.connect(lambda: self.switch_view(TrackEditorWindow))
        view_menu.addAction(track_editor_action)

    def switch_view(cls, new_view_class):
        new_window = new_view_class()
        new_window.show()
        cls._open_windows.append(new_window)

        def handle_close(event):
            cls._open_windows.remove(new_window)
            if not cls._open_windows:
                QApplication.instance().quit()
            super(new_view_class, new_window).closeEvent(event)

        new_window.closeEvent = handle_close

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