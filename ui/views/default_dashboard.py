from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.divider_container import DividerContainer
import logging

logger = logging.getLogger("DefaultDashboard")

class DefaultDashboard(QWidget):
    """
    DefaultDashboard is the default dashboard shown on startup. It contains a root DividerContainer
    and can be customized to show welcome info, quick actions, or a default layout.
    """
    def __init__(self):
        super().__init__()
        logger.debug("[STEP] Creating root DividerContainer for DefaultDashboard")
        self.root_divider = DividerContainer(orientation="vertical")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.root_divider)
        self.setLayout(layout)

    def set_edit_mode(self, edit_mode: bool):
        logger.debug(f"DefaultDashboard.set_edit_mode({edit_mode}) -> root_divider")
        self.root_divider.set_edit_mode(edit_mode)
