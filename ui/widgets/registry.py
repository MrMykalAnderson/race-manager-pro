# Widget registry for dynamic UI addition
# Add new widgets here to make them available in the UI
from .doc_viewer_widget import DocViewerWidget
from .session_summary_widget import SessionSummaryWidget
from .lap_chart_widget import LapChartWidget
from .test_widget import TestWidget

WIDGET_REGISTRY = {
    "Documentation Viewer": DocViewerWidget,
    "Session Summary": SessionSummaryWidget,
    "Lap Chart": LapChartWidget,
    "Test Widget": TestWidget,
    # Add more widgets here as needed
}
