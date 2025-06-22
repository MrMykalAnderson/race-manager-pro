import sys
import math
import json
import os
import shutil

from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsTextItem,
    QMainWindow, QToolBar, QFileDialog, QInputDialog, QMessageBox
)
from PySide6.QtGui import QPainter, QPainterPath, QPen
from PySide6.QtCore import Qt, Signal, QPointF
from PySide6.QtWidgets import QFileDialog, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QAction

from render.qt.track_view import TrackView
from render.qt.track_editor_window import TrackEditorWindow



TRACKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tracks'))


class TrackScene(QGraphicsScene):
    def __init__(self, track_data):
        super().__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.pen_straight = QPen(Qt.black, 2)
        self.pen_corner = QPen(Qt.blue, 2)
        self.draw_track(track_data)

    def draw_track(self, track_data):
        for segment in track_data['segments']:
            label = segment['meta'].get('section', '')

            if segment['type'] == 'straight':
                x0, y0 = segment['start']
                x1, y1 = segment['end']
                self.addLine(x0, -y0, x1, -y1, self.pen_straight)

                # Label midpoint
                mid_x = (x0 + x1) / 2
                mid_y = (y0 + y1) / 2
                text = QGraphicsTextItem(label)
                text.setPos(mid_x, -mid_y)
                self.addItem(text)

            elif segment['type'] == 'corner':
                center_x, center_y = segment['center']
                radius = segment['radius']
                theta1 = segment['start_angle']
                theta2 = segment['end_angle']
                angle_diff = (theta2 - theta1) % 360

                path = QPainterPath()
                steps = 100
                for i in range(steps + 1):
                    angle = math.radians(theta1 + i * angle_diff / steps)
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    if i == 0:
                        path.moveTo(x, -y)
                    else:
                        path.lineTo(x, -y)
                self.addPath(path, self.pen_corner)

                # Label midpoint of arc
                mid_angle = math.radians((theta1 + theta2) / 2)
                label_x = center_x + radius * math.cos(mid_angle)
                label_y = center_y + radius * math.sin(mid_angle)
                text = QGraphicsTextItem(label)
                text.setPos(label_x, -label_y)
                self.addItem(text)




def load_track(filename):
    path = os.path.join(TRACKS_DIR, filename)
    with open(path, 'r') as f:
        return json.load(f)

def add_background_image(scene):
    # Open a file dialog to pick the image
    filename, _ = QFileDialog.getOpenFileName(None, "Select Background Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
    if not filename:
        return

    # Load and add the image to the scene
    pixmap = QPixmap(filename)
    if pixmap.isNull():
        print("Failed to load image.")
        return

    image_item = QGraphicsPixmapItem(pixmap)
    image_item.setZValue(-100)  # Send it to the back
    scene.addItem(image_item)

def main():
    app = QApplication(sys.argv)
    window = TrackEditorWindow()
    window.show()
    sys.exit(app.exec())

def run_track_editor():
    app = QApplication.instance()
    owns_app = app is None
    if owns_app:
        app = QApplication(sys.argv)

    window = TrackEditorWindow()
    window.show()

    if owns_app:
        sys.exit(app.exec())
        
if __name__ == '__main__':
    main()