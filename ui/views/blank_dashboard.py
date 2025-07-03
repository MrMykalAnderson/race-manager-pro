from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.divider_container import DividerContainer
import logging

logger = logging.getLogger("BlankDashboard")

class BlankDashboard(QWidget):
    """
    BlankDashboard is the root dashboard for a tab. It contains a single root DividerContainer,
    which manages all dynamic panels and dividers. All additions/removals go through
    the root divider. No floating buttons; all UI actions are handled via the tab menu.
    """
    def __init__(self):
        super().__init__()
        logger.debug("[STEP] Creating root DividerContainer for BlankDashboard")
        self.root_divider = DividerContainer(orientation="vertical")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.root_divider)
        self.setLayout(layout)

    def add_panel(self, panel_cls):
        """
        Add a new panel (e.g., DocViewerPanel) to the root divider.
        """
        logger.info(f"Adding panel {panel_cls.__name__} to BlankDashboard")
        self.root_divider.add_panel(panel_cls())

    def add_divider(self, orientation="vertical"):
        """
        Add a new DividerContainer to the root divider.
        """
        logger.info(f"Adding DividerContainer ({orientation}) to BlankDashboard")
        self.root_divider.add_divider(orientation=orientation)

    def set_edit_mode(self, edit_mode: bool):
        """
        Propagate edit mode changes to the root divider.
        """
        logger.debug(f"BlankDashboard.set_edit_mode({edit_mode}) -> root_divider")
        self.root_divider.set_edit_mode(edit_mode)
