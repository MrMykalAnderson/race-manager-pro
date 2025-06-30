import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
)
from render.qt.renderer_qtcanvas import create_track_editor_window
from render.qt.base_window import BaseWindow
from render.qt.blank_view_window import BlankViewWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Race Manager Pro")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welcome to Race Manager Pro!"))

        # Button: Track Editor
        self.track_editor_button = QPushButton("Open Track Editor")
        self.track_editor_button.clicked.connect(self.launch_track_editor)
        layout.addWidget(self.track_editor_button)

        # Button: Blank View
        self.blank_view_button = QPushButton("Open Blank View")
        self.blank_view_button.clicked.connect(self.launch_blank_view)
        layout.addWidget(self.blank_view_button)
        self.track_editor_windows = []
        self.setLayout(layout)

        # Keep a list of blank windows
        self.blank_windows = []

    def launch_track_editor(self):
        editor = create_track_editor_window()
        editor.show()
        self.track_editor_windows.append(editor)

    def launch_blank_view(self):
        blank = QWidget()
        blank.setWindowTitle("Blank View")
        blank.setMinimumSize(400, 300)
        blank.show()
        self.blank_windows.append(blank)  # Add to list to prevent garbage collection

def main():
    app = QApplication(sys.argv)
    BaseWindow.open_new_window(BlankViewWindow)  # Open a blank view first
    sys.exit(app.exec())


if __name__ == "__main__":
    main()