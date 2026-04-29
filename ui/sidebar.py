from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QPushButton("Dashboard"))
        layout.addWidget(QPushButton("Sessions"))
        layout.addWidget(QPushButton("Analytics"))

        layout.addStretch()

        self.setLayout(layout)