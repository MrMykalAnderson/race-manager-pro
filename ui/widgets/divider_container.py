import functools
from PySide6.QtWidgets import (
    QWidget, QSplitter, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QLabel
)
from PySide6.QtCore import Qt, QEvent
import logging
from ui.widgets.registry import PANEL_REGISTRY

logger = logging.getLogger("DividerContainer")

class DividerContainer(QFrame):
    """
    DividerContainer is a modular, recursive container for panels and other dividers.
    It manages a QSplitter (vertical or horizontal) and supports dynamic addition
    of panels and nested dividers. Edit mode enables visual cues and wider splitter handles.
    """
    def __init__(self, orientation: str = 'vertical', edit_mode: bool = False):
        super().__init__()
        self.orientation = orientation
        self.edit_mode = edit_mode
        self.children_widgets = []
        self.setMouseTracking(True)
        self._highlight_state = None  # None, 'active', 'ancestor', 'delete'
        self._delete_hover = False
        logger.debug(f"Creating QSplitter orientation={self.orientation}")
        if self.orientation == 'vertical':
            self.splitter = QSplitter(Qt.Vertical)
        else:
            self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.setFrameStyle(QFrame.NoFrame)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        # Centered '+' button for empty containers (no custom style)
        self.center_add_btn = QPushButton("＋", self)
        self.center_add_btn.setToolTip("Add or split")
        self.center_add_btn.setFixedSize(48, 48)
        self.center_add_btn.hide()
        self.center_add_btn.mousePressEvent = self._add_btn_mouse_press
        # Small '×' button for delete in top-right (no custom style)
        self.delete_btn = QPushButton("✕", self)
        self.delete_btn.setToolTip("Delete panel/divider")
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.clicked.connect(self._delete_child)
        self.delete_btn.hide()
        self.delete_btn.installEventFilter(self)
        # Highlight border for hover in edit mode (no custom style)
        self._highlight = QLabel(self)
        self._highlight.hide()
        self.installEventFilter(self)
        self._update_controls()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Center the add button
        cx = (self.width() - self.center_add_btn.width()) // 2
        cy = (self.height() - self.center_add_btn.height()) // 2
        self.center_add_btn.move(cx, cy)
        # Top-right for delete
        self.delete_btn.move(self.width() - self.delete_btn.width() - 8, 8)
        # Highlight border
        self._highlight.resize(self.width(), self.height())

    def eventFilter(self, obj, event):
        if obj == self.delete_btn:
            if event.type() == QEvent.Enter:
                self._set_delete_highlight(True)
            elif event.type() == QEvent.Leave:
                self._set_delete_highlight(False)
            return False
        if event.type() == QEvent.Enter:
            self._set_highlight_chain('active')
        elif event.type() == QEvent.Leave:
            self._set_highlight_chain(None)
        elif event.type() == QEvent.MouseMove:
            self._set_highlight_chain('active')
        return super().eventFilter(obj, event)

    def _set_highlight_chain(self, state):
        # Recursively set highlight on self and all parents
        if self.edit_mode:
            self._set_highlight(state)
            parent = self.parent()
            ancestor_state = 'ancestor' if state == 'active' else None
            while parent:
                if isinstance(parent, DividerContainer):
                    parent._set_highlight(ancestor_state)
                    parent = parent.parent()
                else:
                    break
        else:
            self._set_highlight(None)

    def _set_highlight(self, state):
        self._highlight_state = state
        if state == 'active' and self.edit_mode:
            self._highlight.setStyleSheet("border: 2px solid #1976d2; border-radius: 8px;")
            self._highlight.show()
        elif state == 'ancestor' and self.edit_mode:
            self._highlight.setStyleSheet("border: 2px solid #b0b0b0; border-radius: 8px;")
            self._highlight.show()
        elif state == 'delete' and self.edit_mode:
            self._highlight.setStyleSheet("border: 2px solid #d32f2f; border-radius: 8px;")
            self._highlight.show()
        else:
            self._highlight.hide()

    def _set_delete_highlight(self, value):
        # If deleting a panel, highlight just this container in red
        # If deleting a divider (splitter), highlight both children in red
        if not value:
            self._set_highlight_chain(None)
            # Also clear delete highlight from children if this is a splitter
            for child in self.children_widgets:
                if isinstance(child, DividerContainer):
                    child._set_highlight(None)
            return
        # If this container holds a splitter (i.e., is a divider), highlight both children
        if self.children_widgets and isinstance(self.children_widgets[0], QSplitter):
            for i in range(self.children_widgets[0].count()):
                widget = self.children_widgets[0].widget(i)
                if isinstance(widget, DividerContainer):
                    widget._set_highlight('delete')
        else:
            self._set_highlight('delete')

    def add_child(self, widget):
        for child in self.children_widgets:
            self.splitter.removeWidget(child)
            child.setParent(None)
        self.children_widgets.clear()
        self.splitter.addWidget(widget)
        self.children_widgets.append(widget)
        self._update_controls()
        self.update()

    def add_panel(self, panel: QWidget):
        """
        Add a leaf panel (e.g., DocViewerPanel) to this divider.
        """
        self.add_child(panel)

    def add_divider(self, orientation: str = 'vertical') -> 'DividerContainer':
        """
        Add a nested DividerContainer (divider) to this divider.
        Returns the new divider for further configuration.
        """
        divider = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
        self.add_child(divider)
        return divider

    def _delete_child(self):
        for child in self.children_widgets:
            self.splitter.removeWidget(child)
            child.setParent(None)
        self.children_widgets.clear()
        self._update_controls()
        self.update()

    def set_edit_mode(self, edit_mode: bool):
        """
        Enable or disable edit mode for this divider and propagate to children.
        """
        self.edit_mode = edit_mode
        self._update_controls()
        for child in self.children_widgets:
            if hasattr(child, "set_edit_mode"):
                child.set_edit_mode(edit_mode)

    def _update_controls(self):
        # Show highlight only if edit mode and mouse is over this or a descendant
        # (handled by _set_highlight_chain)
        if not self.edit_mode:
            self.center_add_btn.hide()
            self.delete_btn.hide()
            self._highlight.hide()
            return
        if not self.children_widgets:
            self.center_add_btn.show()
            self.delete_btn.hide()
        else:
            self.center_add_btn.hide()
            self.delete_btn.show()

    def _show_add_menu(self):
        logger.info("[DEBUG] _show_add_menu called, creating menu")
        menu = QMenu(self)
        menu.addAction("Add Panel", self._show_add_panel_menu)
        menu.addAction("Split Horizontally", self._split_horizontal)
        menu.addAction("Split Vertically", self._split_vertical)
        logger.info("[DEBUG] Showing menu (popup) at position: %s", self.center_add_btn.mapToGlobal(self.center_add_btn.rect().bottomLeft()))
        menu.popup(self.center_add_btn.mapToGlobal(self.center_add_btn.rect().bottomLeft()))

    def _show_add_panel_menu(self):
        menu = QMenu(self)
        for name, cls in PANEL_REGISTRY.items():
            action = menu.addAction(name)
            action.triggered.connect(functools.partial(self._add_panel_from_menu, cls))
        menu.popup(self.center_add_btn.mapToGlobal(self.center_add_btn.rect().bottomLeft()))

    def _add_panel_from_menu(self, panel_cls):
        self.add_panel(panel_cls())

    def _split_horizontal(self):
        """Split this divider horizontally."""
        if not self.children_widgets:
            d1 = DividerContainer(orientation='vertical', edit_mode=self.edit_mode)
            d2 = DividerContainer(orientation='vertical', edit_mode=self.edit_mode)
            self.add_child(self._make_splitter(Qt.Horizontal, d1, d2))
        self._update_controls()

    def _split_vertical(self):
        """Split this divider vertically."""
        if not self.children_widgets:
            d1 = DividerContainer(orientation='vertical', edit_mode=self.edit_mode)
            d2 = DividerContainer(orientation='vertical', edit_mode=self.edit_mode)
            self.add_child(self._make_splitter(Qt.Vertical, d1, d2))
        self._update_controls()

    def _make_splitter(self, orientation, d1, d2):
        splitter = QSplitter(orientation)
        splitter.addWidget(d1)
        splitter.addWidget(d2)
        return splitter

    def _split(self, orientation):
        logger.debug(f"[SPLIT] _split called with orientation={orientation} on {self}")
        parent_splitter = self._find_parent_splitter()
        # If this is a leaf divider with a single panel, move that panel to the first new divider
        if len(self.children_widgets) == 1 and not isinstance(self.children_widgets[0], DividerContainer):
            logger.debug(f"[SPLIT] Leaf divider with single panel, moving panel to new divider")
            panel = self.children_widgets.pop()
            self.splitter.removeWidget(panel)
            if parent_splitter is None:
                self.orientation = orientation
                self.splitter.setOrientation(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
                d1 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
                d2 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
                d1.add_child(panel)
                d1.set_edit_mode(self.edit_mode)
                d2.set_edit_mode(self.edit_mode)
                self.splitter.addWidget(d1)
                self.splitter.addWidget(d2)
                self.children_widgets = [d1, d2]
                return
            else:
                new_splitter = QSplitter(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
                d1 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
                d2 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
                d1.add_child(panel)
                d1.set_edit_mode(self.edit_mode)
                d2.set_edit_mode(self.edit_mode)
                new_splitter.addWidget(d1)
                new_splitter.addWidget(d2)
                self._replace_in_parent(new_splitter)
                self.setParent(None)
                return
        # If this divider is empty, just change orientation
        if not self.children_widgets:
            logger.debug(f"[SPLIT] Divider empty, changing orientation to {orientation} for {self}")
            self.orientation = orientation
            self.splitter.setOrientation(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
            return
        # If this is the root and not a leaf, reconfigure self (move all children to first new divider)
        if parent_splitter is None:
            logger.debug(f"[SPLIT] Root divider, reconfiguring self")
            old_widgets = list(self.children_widgets)
            for w in old_widgets:
                self.splitter.removeWidget(w)
            self.children_widgets.clear()
            self.orientation = orientation
            self.splitter.setOrientation(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
            d1 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
            d2 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
            for w in old_widgets:
                d1.add_child(w)
            d1.set_edit_mode(self.edit_mode)
            d2.set_edit_mode(self.edit_mode)
            self.splitter.addWidget(d1)
            self.splitter.addWidget(d2)
            self.children_widgets = [d1, d2]
            return
        # Otherwise, replace self in parent splitter with a new splitter and move all children to first new divider
        logger.debug(f"[SPLIT] Non-root, replacing self in parent splitter")
        new_splitter = QSplitter(Qt.Horizontal if orientation == 'horizontal' else Qt.Vertical)
        d1 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
        d2 = DividerContainer(orientation=orientation, edit_mode=self.edit_mode)
        for w in list(self.children_widgets):
            self.splitter.removeWidget(w)
            d1.add_child(w)
        d1.set_edit_mode(self.edit_mode)
        d2.set_edit_mode(self.edit_mode)
        new_splitter.addWidget(d1)
        new_splitter.addWidget(d2)
        self._replace_in_parent(new_splitter)
        self.setParent(None)
        return

    def _add_btn_mouse_press(self, event):
        logger.info(f"[DEBUG] _add_btn_mouse_press called with event: {event}")
        if event.button() == Qt.LeftButton:
            logger.info("[DEBUG] Left button detected, calling _show_add_menu")
            self._show_add_menu()
        # Removed QPushButton.mousePressEvent(self.center_add_btn, event) to prevent focus/event issues
