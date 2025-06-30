from PySide6.QtWidgets import QLabel
from render.qt.base_window import BaseWindow
from PySide6.QtCore import Qt

class BlankViewWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blank View")

        # Set a basic label in the window
        label = QLabel("This is a blank view window.")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def add_custom_menu_items(self, menu_bar):
        # Optionally add custom menu items just for this window type
        pass  # You could add Debug → Do Something, etc. here