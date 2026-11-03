from PySide6.QtWidgets import QApplication
import sys
from app.utils import config_manager
from views.form_window import MainFormWindow
from  app.views.home_view import HomeAppView
from app.utils.config_manager import ConfigManager
import os
import logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)
logger.debug("")


def app_setup(app, config):
    """
    Method app_setup is used to setup theme , fonts for the application
    """
    theme = config.get("theme")


app = QApplication()
configManager = ConfigManager()
app_folder = configManager.app_dir

# window = MainFormWindow(app, app_folder)
window = HomeAppView("setup_username", "setup_uuid")

window.show()

exit_code = app.exec()
sys.exit(exit_code)