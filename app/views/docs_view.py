"""
docs_view.py

Purpose:
    Provides class DocsView for user documentation


Depends:
    utils.config_manager.ConfigManager

"""
from string import ascii_lowercase

from PySide6.QtCore import Signal
from PySide6.QtGui  import QPixmap, Qt
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QLabel, QScrollArea, QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QGroupBox, QSizePolicy
from app.utils.config_manager import ConfigManager
import logging

# from  rich.logging import RichHandler
logger = logging.getLogger(__name__)
class DocsView(QWidget):
    """
    Class DocsView setups the QWidget window for user documentation 
    """
    closed = Signal()

    def __init__(self):
        """
        DocsView constructor method. Used for initializing class instance
        """
    
        super().__init__()
        self.setWindowTitle("User Documentation")   
        self.config_manager = ConfigManager()
        self.main_layout = QVBoxLayout()
        self._all_widgets = []
        
        # setting scroll_area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()

        
        main_title = QLabel("Welcome to User documentation")
        main_title.setObjectName("mainTitle")
        self.main_layout.addWidget(main_title)


        account_gb = QGroupBox()
        account_gb.setTitle("Account Registration and Login")
        account_gb_layout = QVBoxLayout(account_gb)
        # Add top margin to clear the title
        m = account_gb_layout.contentsMargins()
        account_gb_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())



        self.doc_images_path = self.config_manager.app_dir/"app/resources/images/docs"
        login_path = self.doc_images_path / "login_window_window.png"
        logger.debug('Path to login_image: %s', login_path)
        login_image = QPixmap(self.doc_images_path /"login_window.png")
        login_image_label = QLabel()
        login_image_label.setPixmap(login_image)

        login_description = QLabel("At the start of the application, you can register with your email and password. If you already have an account, login")

        account_gb_layout.addWidget(login_description)
        account_gb_layout.addWidget(login_image_label)



        # HOME VIEW SETUP
        home_view_gb = QGroupBox()
        home_view_gb_layout = QVBoxLayout(home_view_gb)
        m = home_view_gb_layout.contentsMargins()
        home_view_gb_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())
        home_image = QPixmap(self.doc_images_path / "home_window.png")
        scaled_home_image = home_image.scaled(800, 550, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        home_image_label= QLabel()
        home_image_label.setPixmap(scaled_home_image)

        home_image_description = QLabel("The home view provides the user with multiple options. You have 3 grids:\n 1.FastAction Frame: this provides fast utilities for the user such as new project, Manage projects, sychronization, ai_assistant e.t.c .\n 2.The middle view provides a list of the user project which shows the status of the project: passed deadline, completed, active or future.\n 3.The third grid provides a calender, showing the today's date and  upcoming, completed and passed deadline activities.")
        # You can also fitler the projects using the filter above the table which has the text All by default.  You can also  start editing the project or viewing it's tasks through clicking the OPEN button
        home_image_description.setWordWrap(True)
        home_view_gb.setTitle("Home View")
        home_view_gb_layout.addWidget(home_image_description)
        home_view_gb_layout.addWidget(home_image_label)


        # NEW PROJECT DOCS SETUP
        new_project_gb = QGroupBox()
        new_project_gb_layout = QVBoxLayout(new_project_gb)
        m = new_project_gb_layout.contentsMargins()
        new_project_gb_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())
        new_project_title = QLabel('New Project')
        new_project_title.setObjectName("title")
        new_project_image = QPixmap(self.doc_images_path / "new_project_window.png")
        new_project_image_scaled = new_project_image.scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        new_project_label = QLabel()
        new_project_label.setPixmap(new_project_image_scaled)

        new_project_description = QLabel("To add a new project, click on the New Project button in the home view. This opens up a new window from which you enter the project details")
        new_project_gb.setTitle("New Project")
        new_project_gb_layout.addWidget(new_project_description)
        new_project_gb_layout.addWidget(new_project_label)
        


        # MANAGE PROJECTS DOCS
        manage_project_gb = QGroupBox()
        manage_project_gb.setTitle("Manage Projects")
        manage_project_gb_layout = QVBoxLayout(manage_project_gb)
        m = manage_project_gb_layout.contentsMargins()
        manage_project_gb_layout.setContentsMargins(m.left(),m.top() + 40, m.right(), m.bottom())
        manage_all_projects_image = QPixmap(self.doc_images_path / "manage_all_projects.png")
        manage_all_projects_image_scaled = manage_all_projects_image.scaled(800, 550, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        manage_all_projects_label = QLabel()
        manage_projects_description = QLabel("The window above enables the user to manage projects including:\n1. Clicking View Project Info buttons opens up a window from which you can view or edit Project Details. \n2.Clicking View tasks info button, opens up project phases and subtasks window, from which you can view, create , edit or delete project phase and task details  ")
        manage_all_projects_label.setPixmap(manage_all_projects_image_scaled)

        manage_project_gb_layout.addWidget(manage_projects_description)
        manage_project_gb_layout.addWidget(manage_all_projects_label)

        ## Edit_or_VieW Project Images
        edit_view_project_phase_gb = QGroupBox()
        edit_view_project_layout = QVBoxLayout(edit_view_project_phase_gb)

        m = edit_view_project_layout.contentsMargins()
        edit_view_project_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())
        edit_view_project_phase_gb.setTitle("Edit or View Project Details Info")
        edit_or_view_project_image = QPixmap(self.doc_images_path / "edit_or_view_project_window.png")
        edit_or_view_project_image_scaled = edit_or_view_project_image.scaled(800,500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        edit_or_view_project_description = QLabel("The Edit View Project window is used for managing the project details information. The user can view or edit this information.")
        edit_or_view_project_label = QLabel()
        edit_or_view_project_label.setPixmap(edit_or_view_project_image_scaled)

        edit_view_project_layout.addWidget(edit_or_view_project_description)
        edit_view_project_layout.addWidget(edit_or_view_project_label)


        ## Add Phase And Subtasks Images
        add_phase_and_subtask_gb = QGroupBox()
        add_phase_and_subtask_layout = QVBoxLayout(add_phase_and_subtask_gb)
        m = add_phase_and_subtask_layout.contentsMargins()
        add_phase_and_subtask_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())
        add_phase_and_subtask_gb.setTitle("Manage Project Phase and Subtasks")
        add_phase_and_subtasks_image = QPixmap(self.doc_images_path / "add_phase_and_subtasks_window.png")
        add_phase_and_subtasks_image_scaled = add_phase_and_subtasks_image.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        add_phase_and_subtask_description = QLabel("The Manage Phases window is used for managing the project phases and subtasks. It offers various functionalities such as: \n 1.Create Phase and it's subtasks.\n 2.Edit and Delete a single phase and subtasks")
        add_phase_and_subtasks_label = QLabel()
        add_phase_and_subtasks_label.setPixmap(add_phase_and_subtasks_image_scaled)

        add_phase_and_subtask_layout.addWidget(add_phase_and_subtask_description)
        add_phase_and_subtask_layout.addWidget(add_phase_and_subtasks_label)



        # AI ASSISTANT DOCS
        ai_assistant_gb = QGroupBox()
        ai_assistant_gb_layout = QVBoxLayout(ai_assistant_gb)
        m = ai_assistant_gb_layout.contentsMargins()
        ai_assistant_gb_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())
        ai_assistant_gb.setTitle("AI Assistant")
        ai_assistant_image = QPixmap(self.doc_images_path / "ai_assistant_window.png")
        ai_assistant_image_scaled = ai_assistant_image.scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        ai_assistant_label = QLabel()
        ai_assistant_label.setPixmap(ai_assistant_image_scaled)

        ai_assistant_description = QLabel("This window is you AI Chat assistant view, from which you can ask your prefered model/AI questions.")

        ai_assistant_gb.setTitle("AI Assistant")
        ai_assistant_gb_layout.addWidget(ai_assistant_description)
        ai_assistant_gb_layout.addWidget(ai_assistant_label)


        # SYCHRONIZE DOCS



        # SETTINGS DOCS
        settings_gb = QGroupBox()
        settings_gb_layout = QVBoxLayout(settings_gb)

        m = settings_gb_layout.contentsMargins()
        settings_gb_layout.setContentsMargins(m.left(), m.top() + 40, m.right(), m.bottom())
        settings_image = QPixmap(self.doc_images_path / "settings_view.png")
        settings_image_scaled = settings_image.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        settings_label = QLabel()
        settings_label.setPixmap(settings_image_scaled)
        settings_description = QLabel("Clicking Settig button, opens up a window from which you can set your custom settings for the application:\n 1. Dark Mode Setting: set's the theme for the application\n 2.Email address: This email address will be used to send notification to the user incase of project deadline, upcoming project.\n 3.Save Data before exiting: Settig this to True will ensure that the project save all changes, before exiting any window.\n 4.Maximum Window: Sets how Home View should be open  after login.\n 5.Enter mongo url: This is your project url set in mongodb.\n 6.Model Name: You model name you have configured using ollama on your device.\n 7. Export App Data: this exports the entire application data")

        settings_gb.setTitle("Settings")
        settings_gb_layout.addWidget(settings_description) 
        settings_gb_layout.addWidget(settings_label) 



        # PERFORMANCE VIEW


        # for widget in self._all_widgets:
        #     self.scroll_layout.addWidget(widget)



        self.scroll_layout.addWidget(account_gb)
        self.scroll_layout.addWidget(home_view_gb)
        self.scroll_layout.addWidget(new_project_gb)
        self.scroll_layout.addWidget(manage_project_gb)
        self.scroll_layout.addWidget(edit_view_project_phase_gb)
        self.scroll_layout.addWidget(add_phase_and_subtask_gb)
        self.scroll_layout.addWidget(ai_assistant_gb)
        self.scroll_layout.addWidget(settings_gb)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)



        self.setStyleSheet("""
            QLabel#mainTitle {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px
            }
            QGroupBox::title {
                font-size: 28px;
                margin-bottom: 25px;
            }
            QGroupBox {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #292929,
                    stop: 1 #101010
                );
                font-size: 28px;
                border: 1px solid rgba(255, 255, 255, 180);
                border-radius: 10px;
                margin-top: 20px;
                margin-bottom: 20px;
            }

        """)

        self._all_widgets = [account_gb, home_view_gb, new_project_gb, manage_project_gb, edit_view_project_phase_gb, add_phase_and_subtask_gb, ai_assistant_gb, settings_gb]
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 120))

        for groupbox in self._all_widgets:
            groupbox.setGraphicsEffect(shadow)

        self.setLayout(self.main_layout)


    def close_window(self):
        """
        """
        self.close()

    def closeEvent(self, event):
        """
        """
        self.closed.emit()
        super().closeEvent(event)



# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True)],
# )

# app = QApplication([])
# window = DocsView()
# window.show()
# app.exec()