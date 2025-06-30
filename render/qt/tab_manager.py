from PySide6.QtWidgets import QTabWidget


class TabManager(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_tab(self, widget, title=""):
        index = self.addTab(widget, title)
        self.setCurrentIndex(index)
        return index

    def close_tab(self, index):
        widget = self.widget(index)
        self.removeTab(index)
        widget.deleteLater()