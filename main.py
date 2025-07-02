import sys
import logging
import os
import faulthandler
from PySide6.QtWidgets import QApplication
from ui.core.base_window import BaseWindow
from ui.views.blank_view import BlankView

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("main")


def main():
    # Enable faulthandler for segfault tracebacks
    faulthandler.enable()
    # Set Qt debug environment variables for more verbose output
    os.environ["QT_DEBUG_PLUGINS"] = "1"
    os.environ["QT_LOGGING_RULES"] = "qt.*=true"
    logger.info("Starting QApplication...")
    app = QApplication(sys.argv)

    window = BaseWindow()
    window.add_tab(BlankView(), "Blank View")
    window.show()
    logger.info("Window shown, entering event loop...")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()