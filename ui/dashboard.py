from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame


class Card(QFrame):
    def __init__(self, title, value):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel(value)
        self.value.setObjectName("cardValue")

        layout.addWidget(self.title)
        layout.addWidget(self.value)

        self.setLayout(layout)


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.total_minutes = 0
        self.sessions = 0

        layout = QVBoxLayout()

        # Cards row
        row = QHBoxLayout()

        self.total_card = Card("Total Minutes", "0")
        self.sessions_card = Card("Sessions", "0")

        row.addWidget(self.total_card)
        row.addWidget(self.sessions_card)

        layout.addLayout(row)

        # Add button
        self.info = QLabel("Click to simulate study session")
        self.info.setObjectName("infoText")

        layout.addWidget(self.info)

        self.setLayout(layout)

    def add_session(self, minutes):
        self.total_minutes += minutes
        self.sessions += 1

        self.total_card.value.setText(str(self.total_minutes))
        self.sessions_card.value.setText(str(self.sessions))