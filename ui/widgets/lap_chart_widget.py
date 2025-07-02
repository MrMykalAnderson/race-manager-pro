from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout
from .base_widget import BaseWidget
import os
import json
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LapChartWidget(BaseWidget):
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
        self.table.setColumnCount(num_laps)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels([f"Lap {i+1}" for i in range(num_laps)])
        self.table.setVerticalHeaderLabels([r['driver']['name'] for r in results])
        # Build a lap-by-lap position matrix
        lap_times = [[sum(lap['lap_time'] for lap in r['laps'][:lap+1]) for lap in range(num_laps)] for r in results]
        for lap in range(num_laps):
            times_this_lap = [(i, lap_times[i][lap]) for i in range(len(results))]
            times_this_lap.sort(key=lambda x: x[1])
            for pos, (driver_idx, _) in enumerate(times_this_lap, start=1):
                self.table.setItem(driver_idx, lap, QTableWidgetItem(str(pos)))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # Plot lap chart
        self.plot_lap_chart(results, num_laps, lap_times)

    def plot_lap_chart(self, results, num_laps, lap_times):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for i, r in enumerate(results):
            # For each lap, find the position of this driver
            positions = []
            for lap in range(num_laps):
                times_this_lap = [(j, lap_times[j][lap]) for j in range(len(results))]
                times_this_lap.sort(key=lambda x: x[1])
                for pos, (driver_idx, _) in enumerate(times_this_lap, start=1):
                    if driver_idx == i:
                        positions.append(pos)
                        break
            ax.plot(range(1, num_laps+1), positions, marker='o', label=r['driver']['name'])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Position')
        ax.set_title('Lap Chart (lower = better)')
        ax.invert_yaxis()
        ax.legend()
        ax.grid(True, linestyle=':')
        self.canvas.draw()
