from PySide6.QtWidgets import QApplication
import sys
from formWindow import MainFormWindow



app = QApplication()

window = MainFormWindow(app)
window.show()

exit_code = app.exec()
sys.exit(exit_code)