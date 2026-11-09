"""
docs_view.py

Purpose:
    Provides class DocsView for user documentation


Depends:
    utils.config_manager.ConfigManager

"""
from string import ascii_lowercase

from PySide6.QtCore import Signal
from PySide6.QtGui  import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QScrollArea, QTextEdit, QVBoxLayout, QWidget, QGroupBox

from app.utils.config_manager import ConfigManager
import logging

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

        accountTitle = QLabel("Account Registration and Login")
        accountTitle.setObjectName("title")

        self.scroll_layout.addWidget(accountTitle)


        self.doc_images_path = self.config_manager.app_dir/"app/resources/images/docs"
        login_path = self.doc_images_path / "login_window_window.png"
        logger.debug('Path to login_image: %s', login_path)
        login_image = QPixmap(self.doc_images_path /"login_window.png")
        login_image_label = QLabel()
        login_image_label.setPixmap(login_image)

        login_description = QTextEdit("At the start of the application, you can register with your email and password.\nIf you already have an account login")
        login_description.setReadOnly(True)
        self._all_widgets.extend([login_image_label, login_description ])



        # HOME VIEW SETUP
        home_title = QLabel("Home View")
        home_title.setObjectName("title")
        home_image = QPixmap(self.doc_images_path / "home_window.png")
        home_image_label= QLabel()
        home_image_label.setPixmap(home_image)

        home_image_description = QTextEdit("The home view provides the user with multiple options. You have 3 grids:\n 1. FastAction Frame: this provides fast utilities for the user such as new project, Manage projects, sychronization, ai_assistant e.t.c . \n 2. The middle view provides a list of the user project which shows the status of the project: passed deadline, completed, active or future. You can also fitler the projects using the filter above the table which has the text All by default.  You can also  start editing the project or viewing it's tasks through clicking the OPEN button")

        self._all_widgets.extend([home_title, home_image_label, home_image_description])


        # NEW PROJECT DOCS SETUP
        new_project_title = QLabel('New Project')
        new_project_title.setObjectName("title")
        new_project_image = QPixmap(self.doc_images_path / "new_project_window.png")
        new_project_label = QLabel()
        new_project_label.setPixmap(new_project_image)

        new_project_description = QTextEdit("To add a new project, click on the New Project button in the home view. This opens up a new window from which you enter the project details")
        new_project_description.setReadOnly(True)
        self._all_widgets.extend([new_project_title, new_project_label, new_project_description])


        # MANAGE PROJECTS DOCS
        manage_projects_title =QLabel("Manage Projects")
        manage_projects_title.setObjectName("title")
        manage_all_projects_image = QPixmap(self.doc_images_path / "manage_all_projects.png")
        manage_all_projects_label = QLabel()
        manage_all_projects_label.setPixmap(manage_all_projects_image)
        manage_projects_description = QTextEdit("The window above enables the user to manage projects including:\n1. Clicking View Project Info buttons opens up a window from which you can view or edit Project Details. \n2.Clicking View tasks info button, opens up project phases and subtasks window, from which you can view, create , edit or delete project phase and task details  ")
        manage_projects_description.setReadOnly(True)

        self._all_widgets.extend([manage_projects_title, manage_all_projects_label, manage_projects_description])

        ## Edit_or_VieW Project Images
        edit_or_view_project_image = QPixmap(self.doc_images_path / "edit_or_view_project_window.png")
        
        ## Add Phase And Subtasks Images
        add_phase_and_subtasks_image = QPixmap(self.doc_images_path / "add_phase_and_subtasks_window.png")
        

        # AI ASSISTANT DOCS
        ai_assistant_title = QLabel("AI Assistant")
        ai_assistant_title.setObjectName("title")
        ai_assistant_image = QPixmap(self.doc_images_path / "ai_asistant.png")
        ai_assistant_label = QLabel()
        ai_assistant_label.setPixmap(ai_assistant_image)

        ai_assistant_description = QTextEdit("This window is you AI Chat assistant view, from which you can ask your prefered model/AI questions.")
        ai_assistant_description.setReadOnly(True)

        self._all_widgets.extend([ai_assistant_title, ai_assistant_label, ai_assistant_description])


        # SYCHRONIZE DOCS



        # SETTINGS DOCS
        settings_title = QLabel("Settings")
        settings_title.setObjectName("title")
        settings_image = QPixmap(self.doc_images_path / "settings_view.png")
        settings_label = QLabel()
        settings_label.setPixmap(settings_image)
        settings_description = QTextEdit("Clicking Settig button, opens up a window from which you can set your custom settings for the application:\n\t - Dark Mode Setting: set's the theme for the application\n\t2.Email address: This email address will be used to send notification to the user incase of project deadline, upcoming project.\n\tSave Data before exiting: Settig this to True will ensure that the project save all changes, before exiting any window.\n\3.Maximum Window: Sets how Home View should be open  after login.\n\t4.Enter mongo url: This is your project url set in mongodb.\n\t5.Model Name: You model name you have configured using ollama on your device.\n\t6. Export App Data: this exports the entire application data")
        settings_description.setReadOnly(True)

        self._all_widgets.extend([settings_title, settings_label, settings_description])



        # PERFORMANCE VIEW


        for widget in self._all_widgets:
            self.scroll_layout.addWidget(widget)


        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)



        self.setStyleSheet("""
            QLabel#mainTitle {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px
            }

            QLabel#title {
                font-size: 20px;
                margin-bottom:5ps;
            }
        """)
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

