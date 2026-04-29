from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StudyStats Native")
        self.setGeometry(200, 100, 1000, 600)

        container = QWidget()
        layout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar()

        # Main content
        self.dashboard = Dashboard()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.dashboard)

        container.setLayout(layout)
        self.setCentralWidget(container)