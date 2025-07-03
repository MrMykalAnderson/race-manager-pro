# Panel registry for dynamic UI addition
# Add new panels here to make them available in the UI
from .doc_viewer_panel import DocViewerPanel
from .session_summary_panel import SessionSummaryPanel
from .lap_chart_panel import LapChartPanel
from .test_panel import TestPanel

PANEL_REGISTRY = {
    "Documentation Viewer": DocViewerPanel,
    "Session Summary": SessionSummaryPanel,
    "Lap Chart": LapChartPanel,
    "Test Panel": TestPanel,
    # Add more panels here as needed
}
