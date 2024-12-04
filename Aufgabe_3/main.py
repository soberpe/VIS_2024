
import sys
from pyFreeDynMainWindow import pyFreeDynMainWindow

from PySide6.QtWidgets import QApplication

app = QApplication(['pyFreeDyn'])
window = pyFreeDynMainWindow()

window.show()

sys.exit(app.exec())
