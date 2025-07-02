from PySide6.QtWidgets import QLabel
from ui.widgets.base_widget import BaseWidget
from PySide6.QtWidgets import QVBoxLayout


class TestWidget(BaseWidget):
    def __init__(self, title="Test Widget", show_title=True):
        super().__init__(title=title, show_title=show_title)

        label = QLabel("This is a test widget.")
        label.setStyleSheet("font-size: 16px; padding: 10px;")

        self.content_layout.addWidget(label)