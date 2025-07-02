from PySide6.QtWidgets import (
    QWidget, QSplitter, QFrame, QVBoxLayout
)
from PySide6.QtCore import Qt

class LayoutContainer(QFrame):
    def __init__(self, orientation='vertical', edit_mode=False):
        super().__init__()
        self.orientation = orientation
        self.edit_mode = edit_mode
        self.children_widgets = []

        # Use QSplitter for resizable, nestable containers
        if self.orientation == 'vertical':
            self.splitter = QSplitter(Qt.Vertical)
        else:
            self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.setFrameStyle()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def setFrameStyle(self):
        if self.edit_mode:
            self.setStyleSheet("border: 2px dashed #888;")
        else:
            self.setStyleSheet("border: none;")

    def add_child(self, child: QWidget):
        self.children_widgets.append(child)
        self.splitter.addWidget(child)

    def set_splitter_handle_width(self, width: int):
        # Set the handle width for all handles in the splitter
        self.splitter.setHandleWidth(width)

    def set_edit_mode(self, edit_mode: bool):
        self.edit_mode = edit_mode
        self.setFrameStyle()
        # Toggle splitter handle width based on edit mode
        if self.edit_mode:
            self.set_splitter_handle_width(6)  # or your preferred width
        else:
            self.set_splitter_handle_width(0)
        for child in self.children_widgets:
            if hasattr(child, "set_edit_mode"):
                child.set_edit_mode(edit_mode)