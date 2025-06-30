from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from render.qt.track_editor_window import TrackEditorWindow


class BlankView(QWidget):
    def __init__(self, switch_view_callback):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("This is a blank view")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        switch_button = QPushButton("Switch to Track Editor")
        switch_button.clicked.connect(lambda: switch_view_callback(TrackEditorWindow))
        layout.addWidget(switch_button)

        self.setLayout(layout)