import sys
from PySide6.QtWidgets import QApplication
from ui.core.base_window import BaseWindow
from ui.views.blank_view import BlankView


def main():
    print("Starting QApplication...")
    app = QApplication(sys.argv)

    window = BaseWindow()
    window.add_tab(BlankView(), "Blank View")
    window.show()
    print("Window shown, entering event loop...")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()  