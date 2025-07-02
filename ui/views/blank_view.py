from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.test_widget import TestWidget
from ui.widgets.layout_container import LayoutContainer


class BlankView(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_mode = True  # Track current edit mode state
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Outer vertical container (entire view)
        self.outer_container = LayoutContainer(orientation='vertical', edit_mode=self.edit_mode)

        # Full-width widget at the top
        top_widget = TestWidget(title="Top Widget")
        self.outer_container.add_child(top_widget)

        # Nested horizontal container (bottom half)
        inner_container = LayoutContainer(orientation='horizontal', edit_mode=self.edit_mode)
        inner_container.add_child(TestWidget(title="Left Widget"))
        inner_container.add_child(TestWidget(title="Right Widget"))

        # Add nested container to outer
        self.outer_container.add_child(inner_container)

        # Add everything to the main layout
        layout.addWidget(self.outer_container)

    def set_edit_mode(self, value: bool):
        self.edit_mode = value
        if hasattr(self, 'outer_container'):
            self.outer_container.set_edit_mode(value)
        # Propagate to all children if needed
        for child in self.findChildren(QWidget):
            if hasattr(child, 'set_edit_mode') and child is not self:
                child.set_edit_mode(value)