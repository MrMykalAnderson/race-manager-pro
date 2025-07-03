from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout
from .base_panel import BasePanel
import os
import json
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LapChartPanel(BasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_title("Lap Chart")
        self.info_label = QLabel("Lap chart: position per lap (1 = leader)")
        self.content_layout.addWidget(self.info_label)
        self.table = QTableWidget()
        self.content_layout.addWidget(self.table)
        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.content_layout.addWidget(self.canvas)
        self.load_sample_session()

    def load_sample_session(self):
        session_path = os.path.join(
            os.path.dirname(__file__),
            '../../data/sessions/20250702_181847_simple_oval_results.json'
        )
        session_path = os.path.abspath(session_path)
        if not os.path.exists(session_path):
            self.info_label.setText("No session data found.")
            return
        with open(session_path, 'r') as f:
            data = json.load(f)
        self.update_chart(data)

    def update_chart(self, session_data):
        results = session_data.get('results', [])
        if not results:
            self.info_label.setText("No results data.")
            return
        num_laps = len(results[0]['laps'])
        # ...existing code for plotting...
