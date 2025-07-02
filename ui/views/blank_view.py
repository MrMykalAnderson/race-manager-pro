from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.layout_container import LayoutContainer
import logging

logger = logging.getLogger("BlankView")


class BlankView(QWidget):
    """
    BlankView is the root view for a tab. It contains a single root LayoutContainer,
    which manages all dynamic widgets and panels. All additions/removals go through
    the root container. No floating buttons; all UI actions are handled via the tab menu.
    """

    def __init__(self):
        super().__init__()
        logger.debug("[STEP] Creating root LayoutContainer for BlankView")
        self.root_container = LayoutContainer(orientation="vertical")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.root_container)
        self.setLayout(layout)

    def add_widget(self, widget_cls):
        """
        Add a new widget (e.g., DocViewerWidget) to the root container.
        """
        logger.info(f"Adding widget {widget_cls.__name__} to BlankView")
        self.root_container.add_widget(widget_cls())

    def add_container(self, orientation="vertical"):
        """
        Add a new LayoutContainer to the root container.
        """
        logger.info(f"Adding LayoutContainer ({orientation}) to BlankView")
        self.root_container.add_container(orientation=orientation)