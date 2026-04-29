from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.settings import Settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StudyStats Native")
        self.setGeometry(200, 100, 1000, 600)

        container = QWidget()
        layout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar()

        # 🔥 STACKED PAGES
        self.stack = QStackedWidget()

        self.dashboard = Dashboard()
        self.settings = Settings()

        self.stack.addWidget(self.dashboard)  # index 0
        self.stack.addWidget(self.settings)   # index 1

        # Layout
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)  # 👈 makes content take remaining space
        
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 🔥 CONNECT SIDEBAR
        self.sidebar.dashboard_btn.clicked.connect(lambda: self.set_active(0))
        self.sidebar.settings_btn.clicked.connect(lambda: self.set_active(1))
        
    def set_active(self, index):
        self.stack.setCurrentIndex(index)

        # reset styles
        self.sidebar.dashboard_btn.setProperty("active", False)
        self.sidebar.settings_btn.setProperty("active", False)

        # set active
        if index == 0:
            self.sidebar.dashboard_btn.setProperty("active", True)
        elif index == 1:
            self.sidebar.settings_btn.setProperty("active", True)

    # refresh style
        self.sidebar.dashboard_btn.style().unpolish(self.sidebar.dashboard_btn)
        self.sidebar.dashboard_btn.style().polish(self.sidebar.dashboard_btn)

        self.sidebar.settings_btn.style().unpolish(self.sidebar.settings_btn)
        self.sidebar.settings_btn.style().polish(self.sidebar.settings_btn)