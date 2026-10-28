"""
list_all_projects_view.py

Purpose:
    The file list_all_projects_view file is used to provide a widget to view all projects


Depends on: 
    utils/file_operations.FileManager
    views/edit_view_single_project.EditSingleProjectView
    views/tasks_view.TaskViewWidget
Exports:
    ListAllProjects

"""

from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QGroupBox, QHBoxLayout, QApplication
from functools import partial
import logging
from rich.logging import RichHandler

from app.utils.file_operations import FileManager
from app.views.edit_view_single_project import EditSingleProjectView
from app.views.tasks_view import TaskViewWidget

logger = logging.getLogger(__name__)
class ListAllProjects(QWidget):
    """
    Class ListAllProjects is used to list all projects in the app_folder, from which a user can view the project information
    """
    def __init__(self):
        """
        constructor method
        """
        super().__init__()
        self._projects = []
        self.setWindowTitle("View All Projects")
        self.projectView = None
        self.taskView = None
        main_layout = QVBoxLayout()

        title_label = QLabel("View All Projects")
        title_label.setStyleSheet("font-size:20px")
        main_layout.addWidget(title_label)

        # search component 
        searchBtn = QPushButton("Search")
        self.search_project = QLineEdit()
        self.search_project.setPlaceholderText("enter project name to search")

        search_hor_layout = QHBoxLayout()
        search_hor_layout.addWidget(self.search_project)
        search_hor_layout.addWidget(searchBtn)

        main_layout.addLayout(search_hor_layout)

        # project contianer
        projects_container = QGroupBox()
        container_layout = QVBoxLayout()

        # file Manager object
        fileManagerObject = FileManager()
        self._projects = fileManagerObject.read_project_directories()


        if len(self._projects) == 0:
            no_projects_label = QLabel("No projects yet. Add to view projects")
            main_layout.addWidget(no_projects_label)
        else:
            for item in self._projects:
                project_title = QLabel(item["project_title"])
                project_layout = QHBoxLayout() # horizontal layout to hold: project_name, view project info and view task info button
                view_projectBtn = QPushButton("View project info")
                view_taskBtn = QPushButton("View tasks info")
                view_projectBtn.clicked.connect(partial(self.open_project_view, item["project_title"]))
                view_taskBtn.clicked.connect(partial(self.open_task_view, item["project_title"]))
                project_layout.addWidget(project_title)
                project_layout.addWidget(view_projectBtn)
                project_layout.addWidget(view_taskBtn)

                container_layout.addLayout(project_layout)

            # sets the layout for the container
            projects_container.setLayout(container_layout)

            # adds the container to the main_layout
            main_layout.addWidget(projects_container)


        main_layout.addStretch()
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)
        self.setLayout(main_layout)


    def open_task_view(self, project_title):
        """
        Opens tasks_view.TaskViewWidget for the given project

        Args:
            project_title(string): the project title of the project, correlating to a folder in app folder
        """
        logger.debug("this will open task view for a single project")
        if self.taskView is None:
            self.taskView = TaskViewWidget(project_name=project_title)
            self.taskView.closed.connect(self.task_view_closed_handler)
            self.taskView.show()

    def task_view_closed_handler(self):
        if self.taskView is not None:
            self.taskView.close()
            self.taskView = None

    def open_project_view(self, project_title):
        """
        Opens edit_view_single_project.EditSingleProjectView for a single project

        Args:
            project_title(string): the project title of the project, correlating to a folder in app folder
        """
        logger.debug("this will open project view for a single project")

        if self.projectView is None:
            self.projectView = EditSingleProjectView(projectName=project_title)
            self.projectView.closed.connect(self.project_view_closed_handler)
            self.projectView.show()

    def project_view_closed_handler(self):
        if self.projectView is not None:
            self.projectView.close()
            self.projectView = None

    def search_project(self):
        logger.debug("Search for a project")
        search_title = self.search_project.text().trim().lower()


        if search_title == "":
            filtered_project = self._projects

        else:
            filtered_project = [
                project for project in self._projects
                if search_title in project["project_title"].lower()
            ]


    def update_ui(self, filter_project_array):
        logger.debug("updates UI")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
app = QApplication()
window = ListAllProjects()
window.show()
app.exec()


        


