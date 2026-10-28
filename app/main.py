from PySide6.QtWidgets import QApplication
import sys
from views.form_window import MainFormWindow
from  app.views.home_view import HomeAppView
import os
import logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
app = QApplication()
app_folder = os.getcwd()
# window = MainFormWindow(app, app_folder)
window = HomeAppView("setup_username", "setup_uuid")
window.show()

exit_code = app.exec()
sys.exit(exit_code)