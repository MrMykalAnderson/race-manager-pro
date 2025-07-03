from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTabBar,
    QMenu, QToolButton, QInputDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from ui.views.default_dashboard import DefaultDashboard
from ui.widgets.registry import PANEL_REGISTRY


class BaseWindow(QMainWindow):
    edit_mode_changed = Signal(bool)

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowTitle("Race Manager Pro")

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Custom tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_widget.setDocumentMode(True)
        layout.addWidget(self.tab_widget)

        # Add dropdown to the active tab
        self.tab_widget.currentChanged.connect(self.add_dropdown_to_active_tab)

        self.edit_mode = False

    def add_tab(self, widget: QWidget, title: str, start_in_edit_mode=False):
        index = self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentIndex(index)
        self.add_dropdown_to_active_tab(index)
        # Connect edit mode signal to the widget if possible
        if hasattr(widget, "set_edit_mode"):
            self.edit_mode_changed.connect(widget.set_edit_mode)
            widget.set_edit_mode(start_in_edit_mode)

    def add_default_dashboard(self):
        self.add_tab(DefaultDashboard(), "Default Dashboard", start_in_edit_mode=False)

    def add_dropdown_to_active_tab(self, index):
        tab_bar = self.tab_widget.tabBar()

        # Remove any existing dropdowns first
        for i in range(tab_bar.count()):
            tab_bar.setTabButton(i, QTabBar.RightSide, None)

        # Create dropdown only for the active tab
        button = QToolButton()
        button.setPopupMode(QToolButton.InstantPopup)

        menu = QMenu(button)

        # Modular UI: Add Panel/Widget actions in edit mode, before Views submenu
        if self.edit_mode:
            add_panel_v_action = QAction("Add Panel (Vertical)", button)
            add_panel_v_action.triggered.connect(lambda: self._add_panel_to_current_view("vertical"))
            menu.addAction(add_panel_v_action)

            add_panel_h_action = QAction("Add Panel (Horizontal)", button)
            add_panel_h_action.triggered.connect(lambda: self._add_panel_to_current_view("horizontal"))
            menu.addAction(add_panel_h_action)

            # Add Panel submenu for all registered panels
            add_panel_menu = QMenu("Add Panel", button)
            for panel_name, panel_cls in PANEL_REGISTRY.items():
                action = QAction(panel_name, button)
                action.triggered.connect(lambda checked, cls=panel_cls: self._add_panel_to_current_dashboard(cls))
                add_panel_menu.addAction(action)
            menu.addMenu(add_panel_menu)

            menu.addSeparator()

        # Views submenu
        views_menu = QMenu("Views", button)
        new_view_action = QAction("New", button)
        new_view_action.triggered.connect(self.create_new_blank_dashboard)
        views_menu.addAction(new_view_action)
        save_view_action = QAction("Save", button)
        save_view_action.triggered.connect(self.save_current_view)
        views_menu.addAction(save_view_action)
        load_view_action = QAction("Load", button)
        load_view_action.triggered.connect(self.load_view)
        views_menu.addAction(load_view_action)
        rename_view_action = QAction("Rename", button)
        rename_view_action.triggered.connect(self.rename_current_view)
        views_menu.addAction(rename_view_action)
        # Switch to Saved View submenu
        switch_view_menu = QMenu("Switch to ...", button)
        # Add Default View as a selectable option
        default_view_action = QAction("Default View", button)
        default_view_action.triggered.connect(self.switch_current_tab_to_default_dashboard)
        switch_view_menu.addAction(default_view_action)
        # Placeholder: populate with saved views in future
        switch_view_menu.addAction(QAction("No saved views", button))
        views_menu.addMenu(switch_view_menu)
        menu.addMenu(views_menu)

        edit_toggle_action = QAction("Toggle Edit Mode", button)
        edit_toggle_action.triggered.connect(self.toggle_edit_mode)
        menu.addAction(edit_toggle_action)

        button.setMenu(menu)
        tab_bar.setTabButton(index, QTabBar.RightSide, button)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.edit_mode_changed.emit(self.edit_mode)
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, "set_edit_mode"):
            current_widget.set_edit_mode(self.edit_mode)
        # Update the tab dropdown menu to reflect new edit mode state
        self.add_dropdown_to_active_tab(self.tab_widget.currentIndex())

    def create_new_blank_dashboard(self):
        from ui.views.blank_dashboard import BlankDashboard
        self.add_tab(BlankDashboard(), "Blank Dashboard", start_in_edit_mode=True)

    def save_current_view(self):
        print("Save view (not yet implemented)")

    def load_view(self):
        print("Load view (not yet implemented)")

    def rename_current_view(self):
        current_index = self.tab_widget.currentIndex()
        if current_index < 0:
            return
        current_title = self.tab_widget.tabText(current_index)
        new_title, ok = QInputDialog.getText(self, "Rename View", "New view name:", text=current_title)
        if ok and new_title.strip():
            self.tab_widget.setTabText(current_index, new_title.strip())

    def switch_current_tab_to_default_dashboard(self):
        current_index = self.tab_widget.currentIndex()
        if current_index < 0:
            return
        new_widget = DefaultDashboard()
        # Connect edit mode signal
        if hasattr(new_widget, "set_edit_mode"):
            self.edit_mode_changed.connect(new_widget.set_edit_mode)
            new_widget.set_edit_mode(self.edit_mode)
        # Replace widget in current tab
        self.tab_widget.removeTab(current_index)
        self.tab_widget.insertTab(current_index, new_widget, "Default View")
        self.tab_widget.setCurrentIndex(current_index)

    def _add_panel_to_current_view(self, orientation):
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, "add_container"):
            current_widget.add_container(orientation=orientation)

    def _add_panel_to_current_dashboard(self, panel_cls=None):
        current_widget = self.tab_widget.currentWidget()
        if panel_cls is None:
            # fallback for old calls, use DocViewerWidget
            from ui.widgets.doc_viewer_widget import DocViewerWidget
            panel_cls = DocViewerWidget
        if hasattr(current_widget, "add_widget"):
            current_widget.add_widget(panel_cls)