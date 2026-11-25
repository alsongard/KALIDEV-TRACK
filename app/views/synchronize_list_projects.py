"""
synchronize_list_projects.py

Purpose:
    The file list_all_projects_view file is used to provide a widget to view all projects


Depends on: 
    utils/file_operations.FileManager
    utils.config_manager.ConfigManager
    views/edit_view_single_project.EditSingleProjectView
    views/tasks_view.TaskViewWidget
Exports:
    ListAllProjects

"""

import asyncio

from PySide6.QtWidgets import QMessageBox, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QGroupBox, QHBoxLayout, QApplication
from functools import partial
from PySide6.QtCore import Signal
import logging
from rich.logging import RichHandler
from dotenv import load_dotenv
import os

from app.database import project_repository
from app.database.db_manager import DatabaseManager
from app.database.project_repository import ProjectRepository
from app.utils.file_operations import FileManager
from app.views.edit_view_single_project import EditSingleProjectView
from app.views.tasks_view import TaskViewWidget
from app.utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)
class SynchronizeProjectList(QWidget):
    """
    Class SynchronizeProjectList is used to list all projects in the app_folder, from which a user can proceed to sychronize the project
    """
    closed = Signal()
    def __init__(self):
        """
        constructor method
        """
        super().__init__()
        self._projects = []
        self.setWindowTitle("View All Projects")
        self.projectView = None
        self.taskView = None
        self.config_manager_instance = ConfigManager()
        main_layout = QVBoxLayout()

        title_label = QLabel("View All Projects")
        title_label.setStyleSheet("font-size:20px")
        main_layout.addWidget(title_label)

        # search component 
        searchBtn = QPushButton("Search")
        searchBtn.clicked.connect(self.search_project)
        self.project_to_search = QLineEdit()
        self.project_to_search.setPlaceholderText("enter project name to search")

        search_hor_layout = QHBoxLayout()
        search_hor_layout.addWidget(self.project_to_search)
        search_hor_layout.addWidget(searchBtn)

        main_layout.addLayout(search_hor_layout)

        # project contianer
        self.project_container = QGroupBox()
        self.container_layout = QVBoxLayout()

        # file Manager object
        self.fileManager = FileManager()
        self._projects = self.fileManager.read_project_directories()


        if len(self._projects) == 0:
            no_projects_label = QLabel("No projects yet. Add to view projects")
            main_layout.addWidget(no_projects_label)
        else:
            for item in self._projects:
                project_title = QLabel(item["project_title"])
                project_layout = QHBoxLayout() # horizontal layout to hold: project_name, view project info and view task info button
                self.backupBtn = QPushButton("Backup project")
                self.backupBtn.setCheckable(True)
                self.backupBtn.clicked.connect(
                    lambda checked, title=item["project_title"] : self.backup(title, checked)
                )
                project_layout.addWidget(project_title)
                project_layout.addWidget(self.backupBtn)


                self.container_layout.addLayout(project_layout)

            # sets the layout for the container
            self.project_container.setLayout(self.container_layout)

            # adds the container to the main_layout
            main_layout.addWidget(self.project_container)


        main_layout.addStretch()
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)
        self.setLayout(main_layout)


    def search_project(self):
        """
        Method search_project is used to search for a project bases on the ``self.search_project`` QLineEdit input. After finding a project it then passed the project to the 
        ``udpate_ui()`` method, which handles updating the User Interface

        Args:
            None
        """
        logger.debug("Search for a project")
        project_name = self.project_to_search.text().strip().lower()


        if project_name == "":
            filtered_project = self._projects

        else:
            filtered_project = [
                project for project in self._projects
                if project_name in project["project_title"].lower()
            ]

            self.update_ui(filtered_project, project_name)


    def update_ui(self, filter_project_array, search_title):
        """
        The method update_ui is used to update the User Interface for the view.

        - Args:
            - filter_project_array(array) : the array that contains the project data
            - search_title(string): the title of the project being searched 
        """
        logger.debug("updates UI")
        # clear a widget if found in the container_layout or passed the layout to clear_layout function
        item = self.container_layout.takeAt(0)
        widget =item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            self.clear_layout(item.layout())

        # when filter_project_array is empty / no project found
        if len(filter_project_array) == 0:
            empty_label = QLabel(f"No project has been found with the name: {search_title}")
            empty_label.setStyleSheet("color: gray; font-style:italic;")
            self.container_layout.addWidget(empty_label)

            return
        
        # when a project has been found
        for item in filter_project_array:
            project_title = QLabel(item["project_title"])
            project_layout = QHBoxLayout() # horizontal layout to hold: project_name, view project info and view task info button
            self.backupBtn = QPushButton("Backup")
            self.backupBtn.setCheckable(True)
            self.backupBtn.clicked.connect(partial(self.backup, item["project_title"]))

            project_layout.addWidget(project_title)
            project_layout.addWidget(self.backupBtn)

            self.container_layout.addLayout(project_layout)


    # method used to clear widgets in a layout
    def clear_layout(self, given_layout):
        """
        Method clear_layout is used to remove widgets in a layout
        """
        while given_layout.count():
            item = given_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())


    # closeEvent method handler
    def closeEvent(self, event):
        self.closed.emit() # emit event
        super().closeEvent(event)

    def backup(self, project_title, checked):
        logger.debug("Checked: %s", checked)
        if checked:
            asyncio.run(self.synchronize_project(project_title=project_title))

    async def synchronize_project(self, project_title):
        """
        This method is used to synchronize projects details and subtasks to mongodb
        """
        project_title = project_title
        logger.debug("project_title: %s", project_title)
        if project_title is None:
            QMessageBox.warning(
                self, 
                "Warning",
                "Project title empty! Cannot backup unknown project"
            )
            return

        load_dotenv()


       
        mongo_url = self.config_manager_instance.get("mongodb_url")
        logger.debug("mongo url: %s", mongo_url)
        if not mongo_url:
            QMessageBox.information(                                                  
                self,                                                             
                "Information",                                                    
                "No mongo url set! Ensure you have a mongo db connection string to backup your projects.",               
                buttons=QMessageBox.StandardButton.Ok                             
            )                                                                         
            return
        database_manager = DatabaseManager(mongo_url=mongo_url)
        project_repository = ProjectRepository(database_manager) # pass the instance of database manager
         
        project_info_data = self.fileManager.read_single_project_data(project_name=project_title)
        project_phase_data = self.fileManager.read_project_task_file(project_name=project_title)
        project_tags = project_info_data["project_tags"]
        logger.debug("project_tags: %s", project_tags)
        project_tags_array = project_tags.split(" ")
        logger.debug('project_tags_array: %s', project_tags_array)
        project_info_data["project_tags"] = project_tags_array
        project_info_data["initial_project_date_ending"] = project_info_data["project_end_date"]
        project_result = await project_repository.insert_project(project_info_data)
        phase_result = await project_repository.insert_project_phase(project_phase_data)
        

        if phase_result and project_result:
            QMessageBox.information(
                self, 
                "Information", 
                "Project information and phase data has been backup successfully."
            )
            
        self.backupBtn.setChecked(False)

        
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True)],
# )
# app = QApplication()
# window = SynchronizeProjectList()
# window.show()
# app.exec()


        


