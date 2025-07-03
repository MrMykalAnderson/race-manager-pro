from PySide6.QtWidgets import (
    QWidget, QSplitter, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMenu
)
from PySide6.QtCore import Qt
import logging
from ui.widgets.registry import WIDGET_REGISTRY

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

        # Edit mode overlay controls
        self.edit_controls = QWidget(self)
        self.edit_controls.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.edit_controls.setStyleSheet("background: transparent;")
        self.edit_controls_layout = QHBoxLayout(self.edit_controls)
        self.edit_controls_layout.setContentsMargins(0, 0, 0, 0)
        self.edit_controls_layout.setSpacing(2)
        self.btn_split_h = QPushButton("⇆")
        self.btn_split_h.setToolTip("Add horizontal divider")
        self.btn_split_h.setFixedSize(24, 24)
        self.btn_split_h.clicked.connect(self._split_horizontal)
        self.edit_controls_layout.addWidget(self.btn_split_h)
        self.btn_split_v = QPushButton("⇅")
        self.btn_split_v.setToolTip("Add vertical divider")
        self.btn_split_v.setFixedSize(24, 24)
        self.btn_split_v.clicked.connect(self._split_vertical)
        self.edit_controls_layout.addWidget(self.btn_split_v)
        self.btn_add_widget = QPushButton("＋")
        self.btn_add_widget.setToolTip("Add widget")
        self.btn_add_widget.setFixedSize(24, 24)
        self.btn_add_widget.clicked.connect(self._add_widget_menu)
        self.edit_controls_layout.addWidget(self.btn_add_widget)
        self.edit_controls.hide()

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
        # Propagate edit mode to new child immediately
        if hasattr(child, "set_edit_mode"):
            child.set_edit_mode(self.edit_mode)

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
        logger.debug(f"Setting edit mode: {edit_mode} for {self}")
        self.edit_mode = edit_mode
        self.setFrameStyle()
        if self.edit_mode:
            self.set_splitter_handle_width(6)
            self.edit_controls.show()
            logger.debug(f"edit_controls shown: {self.edit_controls.isVisible()} at {self.edit_controls.geometry()}")
            self.edit_controls.update()
            self.update()
        else:
            self.set_splitter_handle_width(2)
            self.edit_controls.hide()
            logger.debug(f"edit_controls hidden: {not self.edit_controls.isVisible()} at {self.edit_controls.geometry()}")
            self.edit_controls.update()
            self.update()
        # Always propagate to all children
        for child in self.children_widgets:
            if hasattr(child, "set_edit_mode"):
                child.set_edit_mode(edit_mode)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Position edit controls in the top-right corner
        if self.edit_controls.isVisible():
            self.edit_controls.setGeometry(self.width() - 80, 4, 76, 28)

    def _split_horizontal(self):
        logger.debug(f"[SPLIT] Split horizontal triggered on {self}")
        self._split('horizontal')

    def _split_vertical(self):
        logger.debug(f"[SPLIT] Split vertical triggered on {self}")
        self._split('vertical')

    def _find_parent_splitter(self):
        parent = self.parentWidget()
        while parent is not None:
            if isinstance(parent, QSplitter):
                return parent
            parent = parent.parentWidget()
        return None

    def _replace_in_parent(self, new_widget):
        parent_splitter = self._find_parent_splitter()
        if parent_splitter is not None:
            idx = parent_splitter.indexOf(self)
            parent_splitter.insertWidget(idx, new_widget)
            parent_splitter.widget(idx + 1).setParent(None)  # Remove self

    def _split(self, orientation):
        logger.debug(f"[SPLIT] _split called with orientation={orientation} on {self}")
        parent_splitter = self._find_parent_splitter()
        # If this is a leaf container with a single widget, move that widget to the first new container
        if len(self.children_widgets) == 1 and not isinstance(self.children_widgets[0], LayoutContainer):
            logger.debug(f"[SPLIT] Leaf container with single widget, moving widget to new container")
            widget = self.children_widgets.pop()
            self.splitter.removeWidget(widget)
            if parent_splitter is None:
                self.orientation = orientation
                self.splitter.setOrientation(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
                c1 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
                c2 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
                c1.add_child(widget)
                c1.set_edit_mode(self.edit_mode)
                c2.set_edit_mode(self.edit_mode)
                self.splitter.addWidget(c1)
                self.splitter.addWidget(c2)
                self.children_widgets = [c1, c2]
                return
            else:
                new_splitter = QSplitter(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
                c1 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
                c2 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
                c1.add_child(widget)
                c1.set_edit_mode(self.edit_mode)
                c2.set_edit_mode(self.edit_mode)
                new_splitter.addWidget(c1)
                new_splitter.addWidget(c2)
                self._replace_in_parent(new_splitter)
                self.setParent(None)
                return
        # If this container is empty, just change orientation
        if not self.children_widgets:
            logger.debug(f"[SPLIT] Container empty, changing orientation to {orientation} for {self}")
            self.orientation = orientation
            self.splitter.setOrientation(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
            return
        # If this is the root and not a leaf, reconfigure self (move all children to first new container)
        if parent_splitter is None:
            logger.debug(f"[SPLIT] Root container, reconfiguring self")
            old_widgets = list(self.children_widgets)
            for w in old_widgets:
                self.splitter.removeWidget(w)
            self.children_widgets.clear()
            self.orientation = orientation
            self.splitter.setOrientation(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
            c1 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
            c2 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
            for w in old_widgets:
                c1.add_child(w)
            c1.set_edit_mode(self.edit_mode)
            c2.set_edit_mode(self.edit_mode)
            self.splitter.addWidget(c1)
            self.splitter.addWidget(c2)
            self.children_widgets = [c1, c2]
            return
        # Otherwise, replace self in parent splitter with a new splitter and move all children to first new container
        logger.debug(f"[SPLIT] Non-root, replacing self in parent splitter")
        new_splitter = QSplitter(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
        c1 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
        c2 = LayoutContainer(orientation=orientation, edit_mode=self.edit_mode)
        for w in list(self.children_widgets):
            self.splitter.removeWidget(w)
            c1.add_child(w)
        c1.set_edit_mode(self.edit_mode)
        c2.set_edit_mode(self.edit_mode)
        new_splitter.addWidget(c1)
        new_splitter.addWidget(c2)
        self._replace_in_parent(new_splitter)
        self.setParent(None)

    def _add_widget_menu(self):
        menu = QMenu(self)
        for name, cls in WIDGET_REGISTRY.items():
            action = menu.addAction(name)
            action.triggered.connect(lambda checked, c=cls: self.add_widget(c()))
        menu.exec(self.btn_add_widget.mapToGlobal(self.btn_add_widget.rect().bottomLeft()))