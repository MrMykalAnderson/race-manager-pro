import os
import json
import shutil
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QFileDialog, QInputDialog, QMessageBox,
    QGraphicsPixmapItem
)
from PySide6.QtGui import QPixmap, QPen, QAction
from PySide6.QtCore import Qt

from render.qt.track_view import TrackView
from render.qt.track_scene import TrackScene

TRACKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tracks'))


class TrackEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Race Manager Pro - Track Editor")

        self.scene = None
        self.view = None
        self.track = {}
        self.reference_image_item = None
        self.calibration_points = []

        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.add_toolbar_actions()
        self.setMinimumSize(800, 600)

    def add_toolbar_actions(self):
        load_image_action = QAction("Load Image", self)
        load_image_action.triggered.connect(self.load_image)
        self.toolbar.addAction(load_image_action)

        load_track_action = QAction("Load Track", self)
        load_track_action.triggered.connect(self.load_track_from_library)
        self.toolbar.addAction(load_track_action)

        save_track_action = QAction("Save Track", self)
        save_track_action.triggered.connect(self.save_track)
        self.toolbar.addAction(save_track_action)

        calibrate_action = QAction("Calibrate", self)
        calibrate_action.triggered.connect(self.enable_calibration_mode)
        self.toolbar.addAction(calibrate_action)

    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not filename:
            return

        pixmap = QPixmap(filename)
        if pixmap.isNull():
            print("Failed to load image.")
            return

        image_item = QGraphicsPixmapItem(pixmap)
        image_item.setZValue(-100)
        self.scene.addItem(image_item)

        self.reference_image_item = image_item

        scale = self.track.get("reference_image", {}).get("scale_m_per_px")
        if scale:
            image_item.setScale(scale)

        if "reference_image" not in self.track:
            self.track["reference_image"] = {}
        self.track["reference_image"]["filename"] = os.path.basename(filename)
        self.track["reference_image"]["original_path"] = filename

    def load_track_from_library(self):
        try:
            all_tracks = [name for name in os.listdir(TRACKS_DIR)
                          if os.path.isdir(os.path.join(TRACKS_DIR, name))]
        except Exception as e:
            print(f"Error accessing track directory: {e}")
            return

        if not all_tracks:
            print("No tracks available to load.")
            return

        name, ok = QInputDialog.getItem(self, "Load Track", "Select a track:", all_tracks, 0, False)
        if not ok or not name:
            return

        track_folder = os.path.join(TRACKS_DIR, name)
        json_path = os.path.join(track_folder, "track.json")

        try:
            with open(json_path, 'r') as f:
                self.track = json.load(f)
        except Exception as e:
            print(f"Failed to load track.json: {e}")
            return

        self.scene = TrackScene(self.track)
        self.view = TrackView(self.scene)
        self.setCentralWidget(self.view)
        self.view.calibration_point_selected.connect(self.on_calibration_point)

        ref_data = self.track.get("reference_image")
        if ref_data:
            ref_path = os.path.join(track_folder, ref_data["filename"])
            pixmap = QPixmap(ref_path)
            if not pixmap.isNull():
                image_item = QGraphicsPixmapItem(pixmap)
                image_item.setZValue(-100)
                image_item.setScale(ref_data.get("scale_m_per_px", 1.0))
                self.scene.addItem(image_item)
                self.reference_image_item = image_item

    def save_track(self):
        if not self.track:
            print("No track data to save.")
            return

        name, ok = QInputDialog.getText(self, "Save Track", "Enter track name:")
        if not ok or not name.strip():
            return

        track_folder = os.path.join(TRACKS_DIR, name.strip())
        os.makedirs(track_folder, exist_ok=True)

        if self.track.get("reference_image"):
            ref_data = self.track["reference_image"]
            original_img_path = ref_data.get("original_path")
            if original_img_path:
                ref_filename = os.path.basename(original_img_path)
                ref_data["filename"] = ref_filename
                dest_img_path = os.path.join(track_folder, ref_filename)
                shutil.copyfile(original_img_path, dest_img_path)

        track_path = os.path.join(track_folder, "track.json")
        with open(track_path, 'w') as f:
            json.dump(self.track, f, indent=2)

        QMessageBox.information(self, "Track Saved", f"Track '{name}' saved successfully.")

    def enable_calibration_mode(self):
        if self.view:
            self.view.set_calibration_mode(True)

    def on_calibration_point(self, point):
        self.calibration_points.append(point)
        if len(self.calibration_points) == 2:
            line = self.scene.addLine(
                self.calibration_points[0].x(), self.calibration_points[0].y(),
                self.calibration_points[1].x(), self.calibration_points[1].y(),
                QPen(Qt.red, 2, Qt.DashLine)
            )

            distance, ok = QInputDialog.getDouble(self, "Calibration", "Enter distance in meters:", 200.0, 0.01, 10000, 2)
            if ok:
                pixel_dist = (self.calibration_points[0] - self.calibration_points[1]).manhattanLength()
                if pixel_dist == 0:
                    print("Calibration points are identical.")
                    return
                scale = distance / pixel_dist
                print(f"Calibration scale: {scale:.6f} meters per pixel")

                if self.reference_image_item:
                    self.reference_image_item.setScale(scale)

                if "reference_image" not in self.track:
                    self.track["reference_image"] = {}
                self.track["reference_image"]["scale_m_per_px"] = scale

            self.calibration_points = []
            self.view.set_calibration_mode(False)
