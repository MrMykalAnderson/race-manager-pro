from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTabBar,
    QMenu, QToolButton, QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
class BaseWidget(QWidget):
    def __init__(self, title="Untitled Widget", show_title=True):
        super().__init__()
        self.title = title
        self.show_title = show_title
        self.edit_mode = False

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Optional title and top bar layout
        self.top_bar = QHBoxLayout()

        if self.show_title:
            self.title_label = QLabel(self.title)
            self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.top_bar.addWidget(self.title_label)

        self.top_bar.addStretch()

        self.edit_button = QPushButton("⚙️")
        self.edit_button.setFixedSize(24, 24)
        self.edit_button.setVisible(False)
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.top_bar.addWidget(self.edit_button)

        self.layout.addLayout(self.top_bar)

        # Dedicated area for content
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)

    def set_edit_mode(self, value: bool):
        self.edit_mode = value
        self.edit_button.setVisible(value)

    def on_edit_clicked(self):
        print(f"Edit clicked for: {self.title}")

    def set_title(self, title: str):
        self.title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)