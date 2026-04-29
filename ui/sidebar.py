from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(200)  # 👈 clean width

        layout = QVBoxLayout()

        title = QLabel("StudyStats")
        title.setObjectName("sidebarTitle")

        self.dashboard_btn = QPushButton("Dashboard")
        self.settings_btn = QPushButton("Settings")

        layout.addWidget(title)
        layout.addSpacing(20)

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        self.setLayout(layout)