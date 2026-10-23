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
from PySide6.QtCore import Qt, QSize, QModelIndex
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

    def add_new_group_box(self):
        print("This recreates and adds a new subTaskGroupBox")
        self.mainLayout.addWidget(self.subTaskGroupBox)

    def save_all_tasks_fun(self):
        print("this button will save all new new tasks")

    def exit_window(self):
        print("Exiting window now")





class TaskViewWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.verticalLayout =  QVBoxLayout()
        self.main_widget = QWidget()


        self.create_task_window = None



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

        createTaskBtn = QPushButton("Create Task")
        createTaskBtn.setObjectName("createTaskBtn")
        createTaskBtn.setCheckable(True)
        saveTaskBtn =  QPushButton('Save Tasks')
        saveTaskBtn.setObjectName("saveTaskBtn")
        deleteTaskBtn = QPushButton("Delete Task")
        deleteTaskBtn.setObjectName("deleteTaskBtn")
        exitViewBtn = QPushButton("Exit")
        exitViewBtn.setObjectName("exitViewBtn")


        createTaskBtn.clicked.connect(self.create_new_task_fun)
        saveTaskBtn.clicked.connect(self.save_task_fun)
        deleteTaskBtn.clicked.connect(self.delete_task_fun)
        exitViewBtn.clicked.connect(self.delete_task_fun)

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


        filename = "/home/alson-kali/PROGRAMMING/KALIDEV-TRACK/research/random_task_data.json"

        # instance of ReadWriteUpdateDeleteFileOperations class
        readTaskInstance = ReadWriteUpdateDeleteFileOperations() 
        returnedTaskData = readTaskInstance.readTaskFiles(filename)

        print("Task read from file")
        print(returnedTaskData)


        print()
        print("-------")
        phase_count = 0

        # trial on using dictionary to set Widgets and Table
        # for item_in_dict in returnedTaskData:

        self.projectName = QLabel()
        self.projectName.setText(returnedTaskData["project"])

        # phases key has the data for table
        for item in  returnedTaskData["phases"]: # item is a dictionary
            self.phaseContentGroupBox = QGroupBox() # GroupBox to enable styling
            self.phaseLayout = QVBoxLayout() # layout for the self.phaseContentGroupBox
            self.phaseTable = QTableView()
            self.phaseTable.wordWrapTrue = True
            
            self.phaseName = QLabel()
            self.phaseName.setObjectName("phaseNameLabel")
            self.phaseName.setText(item["name"])

            self.phaseGoal = QLabel()
            self.phaseGoal.setObjectName("phaseGoalLabel")
            self.phaseGoal.setText(item["goal"])

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
        print("this button is linked to createBtn signal")
        if checked: # true
            if self.create_task_window == None:
                self.create_task_window = CreateTaskWidget()
                self.create_task_window.show()

    def exit_view_fun(self):
        print("this button  is linked to exitBtn signal")


    def save_task_fun(self):
        print("this button is linked to saveBtn signal")


    def delete_task_fun(self):
        print("this button  is  linked to deleteBtn signal")



app = QApplication()
window = TaskViewWidget()
window.show()
app.exec()