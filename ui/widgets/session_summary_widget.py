from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from .base_widget import BaseWidget
import os
import json

class SessionSummaryWidget(BaseWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_title("Session Summary")
        self.info_label = QLabel("Session info will appear here.")
        self.content_layout.addWidget(self.info_label)
        self.table = QTableWidget()
        self.content_layout.addWidget(self.table)
        self.load_sample_session()

    def load_sample_session(self):
        # Load the latest session result file for demo
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
        self.update_summary(data)

    def update_summary(self, session_data):
        # Session info
        track = session_data.get('track', {})
        laps = track.get('laps', 'N/A')
        name = track.get('name', 'N/A')
        self.info_label.setText(f"<b>{name}</b> &mdash; Laps: {laps}")
        # Results table
        results = session_data.get('results', [])
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Pos", "Driver", "Car", "Laps", "Total Time", "Best Lap"
        ])
        self.table.setRowCount(len(results))
        for row, result in enumerate(results):
            driver = result['driver']['name']
            car = result['car']['model']
            laps = len(result['laps'])
            total_time = f"{result['total_time']:.2f}s"
            best_lap = f"{min(l['lap_time'] for l in result['laps']):.2f}s"
            self.table.setItem(row, 0, QTableWidgetItem(str(result['position'])))
            self.table.setItem(row, 1, QTableWidgetItem(driver))
            self.table.setItem(row, 2, QTableWidgetItem(car))
            self.table.setItem(row, 3, QTableWidgetItem(str(laps)))
            self.table.setItem(row, 4, QTableWidgetItem(total_time))
            self.table.setItem(row, 5, QTableWidgetItem(best_lap))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
