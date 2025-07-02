from PySide6.QtWidgets import QWidget
from ui.widgets.layout_container import LayoutContainer
from ui.widgets.session_summary_widget import SessionSummaryWidget
from ui.widgets.lap_chart_widget import LapChartWidget

class DefaultView(QWidget):
    def __init__(self, parent=None, edit_mode=False):
        super().__init__(parent)
        # Create a vertical layout container
        container = LayoutContainer(orientation='vertical', edit_mode=edit_mode)
        # Add SessionSummaryWidget and LapChartWidget
        container.add_child(SessionSummaryWidget())
        container.add_child(LapChartWidget())
        # Set the container as the main layout
        layout = container.layout()
        self.setLayout(layout)

    def set_edit_mode(self, edit_mode: bool):
        # Propagate edit mode to the container and all children
        if self.layout().count() > 0:
            widget = self.layout().itemAt(0).widget()
            if hasattr(widget, 'set_edit_mode'):
                widget.set_edit_mode(edit_mode)
        for child in self.findChildren(QWidget):
            if hasattr(child, 'set_edit_mode') and child is not self:
                child.set_edit_mode(edit_mode)
