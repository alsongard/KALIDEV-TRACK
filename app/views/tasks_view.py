"""
tasks_view.py

Purpose:
    Provides UI Widget for creating and managing phases, subtasks for projects

Depends on:
    - models/tasks_table_model.TaskTableModel
    - views/create_tasks_widget.CreateTaskWidget

Exports: 
    TaskViewWidget
"""


from PySide6.QtWidgets import QTableView, QHBoxLayout, QGridLayout, QLineEdit ,QPushButton, QSizePolicy, QGroupBox, QFrame, QWidget, QApplication, QMainWindow, QLabel,QVBoxLayout, QScrollArea
from  PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QModelIndex, Signal
import sys

# importing classes
from app.utils.file_operations import FileManager
from app.models.tasks_table_model import TaskTableModel
from app.views.create_tasks_widget import CreateTaskWidget

import logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%x]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)



class TaskViewWidget(QWidget):
    """
    TaskViewWidget class provides the User Interface UI for creating and managing tasks

    Attributes:

    Example:
        >>> taskView = TaskViewWidget(project_name="Some project Name")
        >>> taskView.show()
        
    """

    closed = Signal()

    def __init__(self, project_name):
        """
        TaskView Widget constructor method

        Args:
        project_name(string): name of the project

        """
        super().__init__()
        self.verticalLayout =  QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.main_widget = QWidget()
        self.project_name = project_name
        self.create_task_window = None
        self.returned_task_data = {}
        self.setWindowTitle("Manage Project Phases")


        """
        Grid Layout will be added the 2 frames
        meaning 2 columns
        1. fast action frame for fast actions
        2.  main action frame for  displaying the taks  properties and task table
        """
        self.gridLayout = QGridLayout()

        # SETTING UP FAST ACTION FRAME AND FASTACTION LAYOUT
        self.fastActionFrame = QFrame()
        self.fastActionFrame.setStyleSheet("background-color:#0B0B0F;")
        self.fastActionVLayout =  QVBoxLayout()

        createTaskBtn = QPushButton("Add or Create Phase")
        createTaskBtn.setObjectName("createTaskBtn")
        createTaskBtn.setCheckable(True)
        saveTaskBtn =  QPushButton('Save Phases')
        saveTaskBtn.setCheckable(True)
        saveTaskBtn.setObjectName("saveTaskBtn")
        deleteTaskBtn = QPushButton("Delete Phase")
        deleteTaskBtn.setCheckable(True)
        deleteTaskBtn.setObjectName("deleteTaskBtn")
        deleteTaskBtn.setCheckable(True)
        exitViewBtn = QPushButton("Exit")
        exitViewBtn.setObjectName("exitViewBtn")


        createTaskBtn.clicked.connect(self.create_new_task_fun)
        saveTaskBtn.clicked.connect(self.save_task_fun)
        deleteTaskBtn.clicked.connect(self.delete_task_fun)
        exitViewBtn.clicked.connect(self.close_window)

        self.fastActionVLayout.addWidget(createTaskBtn)
        self.fastActionVLayout.addWidget(saveTaskBtn)
        self.fastActionVLayout.addWidget(deleteTaskBtn)
        self.fastActionVLayout.addWidget(exitViewBtn)
        self.fastActionVLayout.addStretch(0)
        self.fastActionFrame.setLayout(self.fastActionVLayout)
        self.fastActionFrameCollapse =  False # used for toggling the fastActionFrame visibility



        # SETTING UP MAIN FRAME AND MAINLAYOUT
        self.mainFrame = QFrame()
        self.mainFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.mainLayout = QVBoxLayout()

        # instance of FileManager class
        readTaskInstance = FileManager() 
        self.returned_task_data = readTaskInstance.read_project_task_file(self.project_name)

        logger.debug("Task read from file: %s", self.returned_task_data)

        # print()
        # print("-------")
        phase_count = 0

        if len(self.returned_task_data) == 0:
            # display something else
            groupBox = QGroupBox()
            descriptionLabel = QLabel(f"No task found for project {self.project_name}\nClick the button below to start adding task for the project!")
            startNewTaskBtn = QPushButton("Create Task")
            startNewTaskBtn.setCheckable(True)
            startNewTaskBtn.clicked.connect(self.create_new_task_fun)

            vert_layout = QVBoxLayout()
            vert_layout.addWidget(descriptionLabel)
            vert_layout.addWidget(startNewTaskBtn)
            groupBox.setLayout(vert_layout)
            self.mainLayout.addWidget(groupBox)
            self.setGeometry(100,100,400,400) 
        else:
            for item in  self.returned_task_data["phases"]: # item is a dictionary
                self.phaseContentGroupBox = QGroupBox() # GroupBox to enable styling
                self.phaseLayout = QVBoxLayout() # layout for the self.phaseContentGroupBox
                self.phaseTable = QTableView() # each subtasks 

                self.phaseTable.wordWrapTrue = True
                
                self.phaseName = QLabel()
                self.phaseName.setObjectName("phaseNameLabel")
                self.phaseName.setText(item["phase name"])

                self.phaseGoal = QLabel()
                self.phaseGoal.setObjectName("phaseGoalLabel")
                self.phaseGoal.setText(item["phase goal"])

                self.phaseLayout.addWidget(self.phaseName)
                self.phaseLayout.addWidget(self.phaseGoal)
                # each_data = []
                # for subtasks in  item["subtasks"]:
                #     print('')

                header_data  = ["Module", "Description", "Status"] 
                self.model = TaskTableModel(item["subtasks"], myHeaderData=header_data )
                self.phaseTable.setModel(self.model)
                self.phaseTable.resizeColumnsToContents()

                self.phaseLayout.addWidget(self.phaseTable)

                self.phaseContentGroupBox.setLayout(self.phaseLayout)
                self.mainLayout.addWidget(self.phaseContentGroupBox)

        # self.projectName = QLabel()
        # self.projectName.setText(self.returned_task_data["project"])




        self.mainFrame.setLayout(self.mainLayout)
        self.fastActionFrame.setFrameShape(QFrame.Shape.Box)
        self.gridLayout.addWidget(self.fastActionFrame, 0, 0)
        self.gridLayout.addWidget(self.mainFrame, 0, 2)

        # self.main_widget.setLayout(self.gridLayout)
        self.setLayout(self.gridLayout)

        
        # self.main_widget.setStyleSheet("""
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QLabel#phaseNameLabel {
                padding-top: 5px;
                padding-bottom: 5px;
                padding-left: 10px;b
                padding-right: 10px;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.1);   /* Semi‑transparent overlay for contrast */
                color: #ffffff;                              /* Adjust text colour for dark background */
                font-size: 18px;
            }
            QLabel#phaseGoalLabel {
                font-style: italic;
                font-size: 14px;
                color: #9BBCE0;
                margin-bottom: 8px;
            }
        """)
    

        # self.setFixedSize(1200,600)
        # self.addWidget(self.main_widget)


    def create_new_task_fun(self, checked):
        logger.debug("this button is linked to createBtn signal")
        if checked: # true
            if self.create_task_window == None:
                self.create_task_window = CreateTaskWidget(self.project_name, self.returned_task_data)
                self.create_task_window.closed.connect(self.on_task_window_close)
                self.create_task_window.setGeometry(150,150, 350,350)
                self.create_task_window.show()

    def close_window(self):
        """
        The method  close_window is used to close the window for task_view
        """
        logger.debug("this function  is linked to exitBtn signal")
        self.close()


    def on_task_window_close(self):
        if self.create_task_window is None:
            return
        else:
            self.create_task_window.close()
            self.create_task_window = None


    def closeEvent(self, event):
        """
        The function closeEvent is used to emit closed signal
        """
        self.closed.emit()
        super().closeEvent(event)

    

    def save_task_fun(self):
        logger.debug("this button is linked to saveBtn signal")


    def delete_task_fun(self):
        logger.debug("this button  is  linked to deleteBtn signal")


# project_name = "KALIDEV-track"


# app = QApplication()
# window = TaskViewWidget(project_name=project_name)
# window.show()
# app.exec()