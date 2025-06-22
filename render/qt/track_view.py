from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, Signal, QPointF


class TrackView(QGraphicsView):
    calibration_point_selected = Signal(QPointF)

    def __init__(self, scene):
        super().__init__(scene)
        self.scale_factor = 1.1
        self.setRenderHint(QPainter.Antialiasing)
        self.setWindowTitle("Qt Track Renderer")
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale(1, 1)

        # Calibration state
        self.calibration_mode = False
        self.calibration_points = []

    def set_calibration_mode(self, enabled):
        self.calibration_mode = enabled
        self.calibration_points = []
        print("Calibration mode:", "ON" if enabled else "OFF")

    def mousePressEvent(self, event):
        if self.calibration_mode and event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.position().toPoint())
            self.calibration_point_selected.emit(scene_pos)
        else:
            super().mousePressEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoom = self.scale_factor
        else:
            zoom = 1 / self.scale_factor

        self.scale(zoom, zoom)
