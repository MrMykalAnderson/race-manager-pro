from PySide6.QtWidgets import QLabel
from ui.widgets.base_panel import BasePanel
from PySide6.QtWidgets import QVBoxLayout

class TestPanel(BasePanel):
    def __init__(self, title="Test Panel", show_title=True):
        super().__init__(title=title, show_title=show_title)
        label = QLabel("This is a test panel.")
        label.setStyleSheet("font-size: 16px; padding: 10px;")
        self.content_layout.addWidget(label)
