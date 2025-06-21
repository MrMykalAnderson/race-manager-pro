from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Race Manager Pro")

layout = QVBoxLayout()
layout.addWidget(QLabel("Welcome to Race Manager Pro!"))

window.setLayout(layout)
window.show()
sys.exit(app.exec())