import sys
import logging
import os
import faulthandler
# Set Qt debug environment variables for more verbose output BEFORE any PySide6 import
os.environ["QT_DEBUG_PLUGINS"] = "1"
os.environ["QT_LOGGING_RULES"] = "qt.*=true"
os.environ["QT_LOGGING_FILE"] = os.path.join(os.path.dirname(__file__), 'race_manager.log')
from PySide6.QtWidgets import QApplication
from ui.core.base_window import BaseWindow
from ui.views.blank_dashboard import BlankDashboard

# Configure logging
logfile = os.path.join(os.path.dirname(__file__), 'race_manager.log')
logging.basicConfig(
    level=logging.INFO,  # Default to INFO for less noise; change to DEBUG for deep troubleshooting
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(logfile, mode='w', encoding='utf-8')
    ]
)
# Direct Qt logging to the same logfile (redundant but safe)
os.environ["QT_LOGGING_FILE"] = logfile
# Silence noisy third-party loggers
logging.getLogger('matplotlib').setLevel(logging.WARNING)
# Set Qt and PySide6 loggers to INFO for more visibility
logging.getLogger('qt').setLevel(logging.INFO)
logging.getLogger('PySide6').setLevel(logging.INFO)
# Set your own modules to DEBUG if needed
logging.getLogger('main').setLevel(logging.INFO)
logging.getLogger('DividerContainer').setLevel(logging.INFO)

logger = logging.getLogger("main")


def main():
    # Enable faulthandler for segfault tracebacks
    faulthandler.enable()
    logger.info("Starting QApplication...")
    app = QApplication(sys.argv)

    window = BaseWindow()
    window.add_tab(BlankDashboard(), "Blank Dashboard")
    window.show()
    logger.info("Window shown, entering event loop...")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()