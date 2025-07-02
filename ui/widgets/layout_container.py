from PySide6.QtWidgets import (
    QWidget, QSplitter, QFrame, QVBoxLayout
)
from PySide6.QtCore import Qt
import logging

logger = logging.getLogger("LayoutContainer")

class LayoutContainer(QFrame):
    """
    LayoutContainer is a modular, recursive container for widgets and panels.
    It manages a QSplitter (vertical or horizontal) and supports dynamic addition
    of widgets and nested containers. Edit mode enables visual cues and wider splitter handles.
    """
    def __init__(self, orientation: str = 'vertical', edit_mode: bool = False):
        super().__init__()
        self.orientation = orientation
        self.edit_mode = edit_mode
        self.children_widgets = []  # Track children for recursive operations

        logger.debug(f"Creating QSplitter orientation={self.orientation}")
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
        """
        Add a child widget or container to the splitter.
        """
        logger.info(f"Adding child widget: {type(child).__name__}")
        self.children_widgets.append(child)
        self.splitter.addWidget(child)

    def add_widget(self, widget: QWidget):
        """
        Add a leaf widget (e.g., DocViewerWidget) to this container.
        """
        self.add_child(widget)

    def add_container(self, orientation: str = 'vertical') -> 'LayoutContainer':
        """
        Add a nested LayoutContainer (panel) to this container.
        Returns the new container for further configuration.
        """
        container = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
        self.add_child(container)
        return container

    def set_splitter_handle_width(self, width: int):
        self.splitter.setHandleWidth(width)

    def set_edit_mode(self, edit_mode: bool):
        logger.debug(f"Setting edit mode: {edit_mode}")
        self.edit_mode = edit_mode
        self.setFrameStyle()
        if self.edit_mode:
            self.set_splitter_handle_width(6)
        else:
            self.set_splitter_handle_width(2)  # Use a small but usable width
        for child in self.children_widgets:
            if hasattr(child, "set_edit_mode"):
                child.set_edit_mode(edit_mode)