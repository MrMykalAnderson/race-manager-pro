from render.qt.base_window import BaseWindow
from render.qt.blank_view import BlankView


class BlankViewWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.tab_manager.add_tab(BlankView(self.switch_view), "Blank View")
