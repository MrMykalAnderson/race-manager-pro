import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
)
from render.qt.renderer_qtcanvas import run_track_editor


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

        self.setLayout(layout)

    def launch_track_editor(self):
        run_track_editor()

    def launch_blank_view(self):
        blank = QWidget()
        blank.setWindowTitle("Blank View")
        blank.setMinimumSize(400, 300)
        blank.show()
        # Keep a reference to prevent garbage collection
        self._blank_window = blank


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()