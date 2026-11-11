from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QToolBar
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import logging
from  rich.logging import RichHandler


logger = logging.getLogger(__name__)
class MainWindow(QMainWindow):
    """
    """
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        menu  = self.menuBar()


        documentation_action = QAction("Documentation", self)
        documentation_action.setCheckable(True)

        about_action = QAction("About", self)
        about_action.setCheckable(True)
        about_action.triggered.connect(self.open_about_view)



        file_action = QAction("File", self)
        file_action.triggered.connect(self.open_file_manager_app)
        file_menu = menu.addMenu("&File")
        file_menu.addAction(file_action)


        help_menu = menu.addMenu("&Help")
        help_menu.addAction(about_action)
        help_menu.addAction(documentation_action)

        main_layout.addWidget(QLabel("Trial using menuBar"))

        self.setLayout(main_layout)
    
    def open_about_view(self):
        """
        """
        logger.debug("Opening documentation view")

    def open_file_manager_app(self):
        """
        """
        logger.debug("Openning file manager")




# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("My App")

#         label = QLabel("Hello!")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         self.setCentralWidget(label)

#         # toolbar = QToolBar("My main toolbar")
#         # toolbar.setIconSize(QSize(16, 16))
#         # self.addToolBar(toolbar)

#         button_action = QAction(QIcon("bug.png"), "&Your button", self)
#         button_action.setStatusTip("This is your button")
#         button_action.triggered.connect(self.toolbar_button_clicked)
#         button_action.setCheckable(True)
#         # toolbar.addAction(button_action)

#         # toolbar.addSeparator()

#         # button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
#         # button_action2.setStatusTip("This is your button2")
#         # button_action2.triggered.connect(self.toolbar_button_clicked)
#         # button_action2.setCheckable(True)
#         # toolbar.addAction(button_action2)

#         # toolbar.addWidget(QLabel("Hello"))
#         # toolbar.addWidget(QCheckBox())

#         # self.setStatusBar(QStatusBar(self))

#         menu = self.menuBar()

#         file_menu = menu.addMenu("&File")
#         file_menu.addAction(button_action)

#     def toolbar_button_clicked(self, s):
#         print("click", s)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()