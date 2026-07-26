from PySide6.QtWidgets import QApplication
import sys
from formWindow import MainFormWindow
import os


app = QApplication()
app_folder = os.getcwd()
window = MainFormWindow(app, app_folder)
window.show()

exit_code = app.exec()
sys.exit(exit_code)