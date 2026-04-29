import sys
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

# 🔥 Fix taskbar icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("studystats.app")

app = QApplication(sys.argv)

app.setWindowIcon(QIcon("assets/icons/app.ico"))

with open("styles/main.qss", "r") as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()

sys.exit(app.exec())