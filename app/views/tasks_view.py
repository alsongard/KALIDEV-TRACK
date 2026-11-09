"""
tasks_view.py

Purpose:
    Provides UI Widget for creating and managing phases, subtasks for projects

Depends on:
    - models/tasks_table_model.TaskTableModel
    - views/create_tasks_widget.CreateTaskWidget
    - utils/file_operations.FileManager

Exports: 
    TaskViewWidget
"""


from PySide6.QtWidgets import QMessageBox, QTableView, QHBoxLayout, QGridLayout, QLineEdit ,QPushButton, QSizePolicy, QGroupBox, QFrame, QWidget, QApplication, QMainWindow, QLabel,QVBoxLayout, QScrollArea
from  PySide6 import QtCore
from PySide6.QtCore import Qt, Signal
import sys

# importing classes
from app.utils.file_operations import FileManager
from app.models.tasks_table_model import TaskTableModel
from app.views.create_tasks_widget import CreateTaskWidget
from functools import partial   

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
        self.subtasks_model_array = []
        self.phase_content_groupbox_array =[]
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
        deleteTaskBtn = QPushButton("Delete All Phase")
        deleteTaskBtn.setCheckable(True)
        deleteTaskBtn.setObjectName("deleteTaskBtn")
        deleteTaskBtn.setCheckable(True)
        exitViewBtn = QPushButton("Exit")
        exitViewBtn.setObjectName("exitViewBtn")


        createTaskBtn.clicked.connect(self.create_new_task_fun)
        saveTaskBtn.clicked.connect(self.save_task_fun)
        deleteTaskBtn.clicked.connect(self.delete_all_phases)
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
        self.scroll_area = QScrollArea() # scroll_area used for scrolling
        self.scroll_widget = QWidget() # scroll_widget that is set for the scroll_area
        self.vert_layout = QVBoxLayout() # layout used by scroll_widget
        
        # instance of FileManager class
        self.fileManager = FileManager() 
        self.returned_task_data = self.fileManager.read_project_task_file(self.project_name)

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

                self.phaseTable.setWordWrap(True)
                self.phaseTable.resizeRowsToContents()
                self.phaseTable.verticalHeader().setDefaultSectionSize(40)
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

                self.header_data  = ["Module", "Description", "Status"] 
                self.model = TaskTableModel(item["subtasks"], myHeaderData=self.header_data) # we set data to the entire subtasks array.
                self.subtasks_model_array.append(self.model) # we then append this model to model_array, which means it holds the entire subtasks for a phase
                self.phaseTable.setModel(self.model)
                self.phaseTable.resizeColumnsToContents()

                self.phaseLayout.addWidget(self.phaseTable)
                button_horizontal_layout = QHBoxLayout()
                self.insertBtn = QPushButton("Insert Row")
                self.removeBtn = QPushButton("Remove Row")
                self.deleteBtn = QPushButton("Delete Phase")

                self.deleteBtn.clicked.connect(self.delete_single_phase)
                self.insertBtn.clicked.connect(partial(self.insert_row, self.model))
                self.removeBtn.clicked.connect(partial(self.remove_row, self.model, self.phaseTable))

                button_horizontal_layout.addWidget(self.deleteBtn, alignment=Qt.AlignmentFlag.AlignLeft)
                button_horizontal_layout.addWidget(self.insertBtn, alignment=Qt.AlignmentFlag.AlignLeft)
                button_horizontal_layout.addWidget(self.removeBtn, alignment=Qt.AlignmentFlag.AlignLeft)
                button_horizontal_layout.addStretch(0)

                self.phaseLayout.addLayout(button_horizontal_layout)

                self.phaseContentGroupBox.setMinimumSize(200, 250)
                self.phaseContentGroupBox.setLayout(self.phaseLayout) # phaseContentGroupBox layout is set
                # self.mainLayout.addWidget(self.phaseContentGroupBox)
                self.phase_content_groupbox_array.append(self.phaseContentGroupBox)
                self.vert_layout.addWidget(self.phaseContentGroupBox) # add to vertial layout

        # self.projectName = QLabel()
        # self.projectName.setText(self.returned_task_data["project"])

        self.scroll_widget.setLayout(self.vert_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)

        self.mainLayout.addWidget(self.scroll_area)
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
        """
        Method save_task_fun is used to save changes after user has edited subtasks for the project phases
        """
        logger.debug("this button is linked to saveBtn signal")
        project_phases = {
            "project" : self.project_name, 
            "phases": []
        }
        
        # for count in range(len(self.phase_content_groupbox_array)):
        count = 0
        # while count < len(self.phase_content_groupbox_array): changed logic to uze zip
        for phase_gb, model in zip(self.phase_content_groupbox_array, self.subtasks_model_array):
            phase_gb = self.phase_content_groupbox_array[count] # phase groupbox
            phase_name = phase_gb.findChild(QLabel, "phaseNameLabel").text() # using objectName to find the specific QLabel 
            phase_description = phase_gb.findChild(QLabel, "phaseGoalLabel").text()
            if not phase_name:
                phase_name  = "Unknow Phase"
            if not phase_description:
                phase_description = "Unknown phase and description"

            logger.debug("phase name: %s", phase_name)
            logger.debug("phase goal: %s", phase_description)
            phase_item = {
                "phase name" : phase_name,
                "phase goal": phase_description,
                "subtasks" : [

                ]
            } # it is better to access the table in the model

            for row in range(model.rowCount()): # number of rows in the table : number of subtasks dictionaries
                subtask_dict = {}
                for column in range(model.columnCount()):
                    # get the dictionary
                    cell_address = model.index(row, column)
                    value = model.data(cell_address, Qt.ItemDataRole.DisplayRole)
                    key = self.header_data[column]
                    logger.debug("key: %s : value: %s", key,value)
                    subtask_dict[key] = value
                    # in this iteration it completes the entire row (a  single dictionary key:values pair)
                
                phase_item["subtasks"].append(subtask_dict)
            
            project_phases["phases"].append(phase_item)
            count +=1 

        logger.debug("project phases: %s", project_phases)

        result = self.fileManager.update_project_tasks(self.project_name, data=project_phases)

        if result:
            QMessageBox.information(
                self,
                "Information",
                "Project tasks updated successfully.",
                buttons=QMessageBox.StandardButton.Ok
            )
        else:
            QMessageBox.information(
                self,
                "Warning", 
                "Project tasks not updated! Contact Support",
                buttons=QMessageBox.StandardButton.Ok
            )

    def delete_all_phases(self):
        """
        Method delete_all_phases is used to remove all project phases in project_task.json
        """
        logger.debug("this button  is  linked to deleteBtn signal")
        response = QMessageBox.warning(
            self,
            "Warning",
            "Are you sure you want to delete all the project phases ? This action cannot be reversed!!",
            buttons = QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        if response:
            logger.debug("all project phases removed")
        else: 
            logger.debug("Action canceled!")


    def delete_single_phase(self):
        """
        Method delete_single_phase is used to remove a single phase from project phases
        """
        logger.debug("removing project phase: someName")

    def insert_row(self, model):
        """
        Method insert_row is a button slot function that is used for inserting rows to a table.
        Inserts a row at the end of the table
        """
        model.insertRows(model.rowCount(), 1)
            


    def remove_row(self, model, table):
        """
        Method remove_row is a button sot function that is used for removing rows to a table
        """
        index = table.currentIndex() # retrieves the  QModelIndex of the row
        if index.isValid():
            model.removeRows(index.row(), 1)
        else:
            QMessageBox.information(
                self,
                "Information", 
                "Select a row to be removed", 
                buttons=QMessageBox.StandardButton.Ok   
            )



# project_name = "KALIDEV-track"


# app = QApplication()
# window = TaskViewWidget(project_name=project_name)
# window.show()
# app.exec()