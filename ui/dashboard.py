from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QFrame, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem
)
from datetime import datetime, timedelta
from collections import defaultdict

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.database import add_session, get_sessions


# -------------------
# CARD COMPONENT
# -------------------
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


# -------------------
# GRAPH COMPONENT
# -------------------
class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_graph(self, sessions):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # DARK THEME
        self.figure.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#161b22")

        # -------------------
        # CURRENT WEEK
        # -------------------
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())

        week_dates = []
        week_labels = []
        week_data = {}

        for i in range(7):
            day = start_of_week + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            label = day.strftime("%a")

            week_dates.append(date_str)
            week_labels.append(label)
            week_data[date_str] = 0

        # -------------------
        # FILL DATA
        # -------------------
        for date, minutes, subject in sessions:
            if date in week_data:
                week_data[date] += minutes

        values = [week_data[d] for d in week_dates]

        # -------------------
        # DRAW
        # -------------------
        ax.bar(week_labels, values, color="#d4af5f")

        ax.set_title("This Week", color="#f0f6fc")
        ax.set_ylabel("Minutes", color="#8b949e")

        ax.tick_params(axis='x', colors="#8b949e")
        ax.tick_params(axis='y', colors="#8b949e")

        for spine in ax.spines.values():
            spine.set_visible(False)

        # EMPTY STATE TEXT
        if all(v == 0 for v in values):
            ax.text(
                0.5, 0.5, "No data yet",
                color="#8b949e",
                ha='center', va='center',
                transform=ax.transAxes
            )

        self.canvas.draw()


# -------------------
# DASHBOARD
# -------------------
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.total_minutes = 0
        self.sessions = 0

        # 🔥 LOAD FROM DATABASE
        self.session_list = get_sessions()

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # -------------------
        # CARDS
        # -------------------
        row = QHBoxLayout()
        row.setSpacing(15)

        self.total_card = Card("Total Minutes", "0")
        self.sessions_card = Card("Sessions", "0")

        row.addWidget(self.total_card)
        row.addWidget(self.sessions_card)

        layout.addLayout(row)

        # -------------------
        # FORM
        # -------------------
        self.minutes_input = QLineEdit()
        self.minutes_input.setPlaceholderText("Minutes studied")

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")

        self.button = QPushButton("Add Session")
        self.button.clicked.connect(self.handle_add)

        layout.addWidget(self.minutes_input)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.button)

        # -------------------
        # TABLE
        # -------------------
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Date", "Minutes", "Subject"])

        # 🔥 LOAD DATA INTO TABLE
        for date, minutes, subject in self.session_list:
            self.total_minutes += minutes
            self.sessions += 1

            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(str(minutes)))
            self.table.setItem(row, 2, QTableWidgetItem(subject))

        self.total_card.value.setText(str(self.total_minutes))
        self.sessions_card.value.setText(str(self.sessions))

        # -------------------
        # GRAPH + TABLE
        # -------------------
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        bottom_layout.addWidget(self.table, 2)

        self.graph = GraphWidget()
        self.graph.setObjectName("graphBox")

        bottom_layout.addWidget(self.graph, 1)

        layout.addLayout(bottom_layout)

        # -------------------
        # INFO
        # -------------------
        self.info = QLabel("")
        self.info.setObjectName("infoText")

        layout.addWidget(self.info)

        self.setLayout(layout)

        # 🔥 DRAW GRAPH ON START
        self.graph.update_graph(self.session_list)

    # -------------------
    # ADD SESSION
    # -------------------
    def handle_add(self):
        minutes_text = self.minutes_input.text()
        subject = self.subject_input.text().strip()

        if not minutes_text.isdigit():
            self.info.setText("❌ Enter valid minutes")
            return

        if subject == "":
            self.info.setText("❌ Enter a subject")
            return

        minutes = int(minutes_text)

        if minutes <= 0:
            self.info.setText("❌ Must be > 0")
            return

        date = datetime.now().strftime("%Y-%m-%d")

        session = (date, minutes, subject)
        self.session_list.append(session)

        # 🔥 SAVE TO DATABASE
        add_session(date, minutes, subject)

        # UPDATE STATS
        self.total_minutes += minutes
        self.sessions += 1

        self.total_card.value.setText(str(self.total_minutes))
        self.sessions_card.value.setText(str(self.sessions))

        # UPDATE TABLE
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(date))
        self.table.setItem(row, 1, QTableWidgetItem(str(minutes)))
        self.table.setItem(row, 2, QTableWidgetItem(subject))

        # UPDATE GRAPH
        self.graph.update_graph(self.session_list)

        # FEEDBACK
        self.info.setText("✅ Session added")

        self.minutes_input.clear()
        self.subject_input.clear()