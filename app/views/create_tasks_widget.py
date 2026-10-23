"""
create_tasks_widget.py

Purpose:
    This file provides the class CreateTaskWidget used for adding phases and subtasks

Depends on:
    - utis/file_operations.FileManager

Exports: 
    CreateTaskWidget
"""

from PySide6.QtWidgets import QWidget, QComboBox,QScrollArea, QMessageBox, QApplication, QSizePolicy, QPushButton, QLabel, QLineEdit, QTextEdit, QFrame, QVBoxLayout, QHBoxLayout, QTableView, QGridLayout , QSizePolicy, QGroupBox, QMainWindow, QVBoxLayout
from  PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QModelIndex, Signal
import sys
import os
import json
 
# importing classes
from app.utils.file_operations import FileManager


import logging 
logger = logging.getLogger(__name__)

class CreateTaskWidget(QWidget):
    """
    CreateTaskWidget provides a window for creating  or adding the phases and subtasks for a project

    Attributes:
        UI Components from PySide6

    Example: 
        >>> taskWidget = CreateTaskWidget()
        >>> taskWidget.show()

    """
    closed = Signal() # a custom signal emitted to Parent Widget (the widget that creates instance of this class)
    logger.info("CreateTaskWidget Instance created")
    def __init__(self, projectName, prev_task_data):
        """
        Constructor method for the class
        """

        super().__init__()
        self.setWindowTitle("Add Phase and subtasks")
        self.fileManager = FileManager()
        self.project_name = projectName
        self.main_layout =  QVBoxLayout() # main layout
        self.scroll_area = QScrollArea() # QScrollArea is used to hold the gb
        self.subtask_container_widget = QWidget() # this is the widget that is added to ScrollArea and contains the groupBox
        self.subtask_container_layout = QVBoxLayout() # this is the layout for subtask_container_widget
        self.sub_task_count = 1
        self.gb_array = [] # array for group_boxes:gb
        self.module_name_inp_array = []
        self.module_description_inp_array = []
        self.module_status_array = []
        self.module_status_note_inp_array = []
        self.subtask_groupboxes = []
        self.prev_task_data = prev_task_data

        # settings for QScrollArea
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        # settigns for subtask_container_layout:QVBoxLayout
        self.subtask_container_layout.setContentsMargins(4, 4, 4, 4)
        self.subtask_container_layout.setSpacing(8)
        self.subtask_container_layout.addStretch(1)


        
        phaseName =  QLabel("Enter Phase/Task Name: ")
        phaseGoal = QLabel("Enter goal name: ")
        self.phase_name_input = QLineEdit()
        self.phase_goal_input = QLineEdit()

        self.main_layout.addWidget(phaseName)
        self.main_layout.addWidget(self.phase_name_input)
        self.main_layout.addWidget(phaseGoal)
        self.main_layout.addWidget(self.phase_goal_input)

        addSubTaskBtn = QPushButton("Add SubTask")
        addSubTaskBtn.setCheckable(True)
        addSubTaskBtn.clicked.connect(self.add_new_group_box)
        self.main_layout.addWidget(addSubTaskBtn)

        # adding UI components to  to self.subtask_container_layout
        self.add_subtask_group() # This method adds the QGroupBox, QVBoxLayout for the groupBox, the Widgets for the subtask
        
        # set layout for the subtask_container_widget
        self.subtask_container_widget.setLayout(self.subtask_container_layout)
        
        # add widget to scroll_area
        self.scroll_area.setWidget(self.subtask_container_widget)
        
        # add the scroll_area to main_layout
        self.main_layout.addWidget(self.scroll_area, 1)



        # buttons for QGroupBox
        exitBtn = QPushButton('Exit')
        exitBtn.setCheckable(True)
        exitBtn.clicked.connect(self.exit_window)

        saveAllTasksBtn = QPushButton("Save Phase")
        saveAllTasksBtn.setCheckable(True)
        saveAllTasksBtn.clicked.connect(self.save_all_tasks_fun)


        horButtonLayout = QHBoxLayout()
        horButtonLayout.addWidget(saveAllTasksBtn)
        horButtonLayout.addWidget(exitBtn)
        self.main_layout.addLayout(horButtonLayout)


        self.setLayout(self.main_layout)


    def add_subtask_group(self):
        """
        The method add_subtask_group is used to add the QGroupBox, the gb_layout, and all components needed for a subtask
        Finally, it adds the input components to their respective arrays e.g self.module_status_array e.t.c
        """
        gb = QGroupBox(f"Subtask {self.sub_task_count}")
        gb_layout = QVBoxLayout()

        module_name =  QLabel("Module/File name")
        module_description = QLabel("Module Description")
        module_status = QLabel("Module Status")
        module_status_note = QLabel("Module Status Note")
    
        module_name_input = QLineEdit()
        module_description_input = QLineEdit()
        module_status_selector = QComboBox()
        module_status_selector.addItems(["Pending", "Completed", "In Progress"])
        module_status_note_input = QLineEdit()

        gb_layout.addWidget(module_name)
        gb_layout.addWidget(module_name_input)
        gb_layout.addWidget(module_description)
        gb_layout.addWidget(module_description_input)
        gb_layout.addWidget(module_status)
        gb_layout.addWidget(module_status_selector)
        gb_layout.addWidget(module_status_note)
        gb_layout.addWidget(module_status_note_input)

        delete_btn = QPushButton("Delete SubTask")
        delete_btn.clicked.connect(lambda _, g=gb: self.remove_groupbox(g))
        gb_layout.addWidget(delete_btn)
        gb.setLayout(gb_layout) # set the layout for the groupbox
        self.subtask_container_layout.insertWidget(self.subtask_container_layout.count() - 1, gb)
        # self.subtask_container_layout.addWidget(gb)
        

        self.module_name_inp_array.append(module_name_input)
        self.module_description_inp_array.append(module_description_input)
        self.module_status_array.append(module_status_selector) # QComboBox : retrieve text using currentText() method
        self.module_status_note_inp_array.append(module_status_note_input)

        self.subtask_groupboxes.append(gb)
        self.sub_task_count += 1
        # self.scroll_area.ensureWidgetVisible(gb)

    def add_new_group_box(self):
        """
        The method add_new_group_box is used to add a QGroubBox component that contains
        the input fields for a sub task
        """
        logger.info("This recreates and adds a new subTaskGroupBox")
        self.add_subtask_group()


    def remove_groupbox(self, gb):
        """
        The method remove_groupbox is used to delete and remove the groupBox from the layout
        """
        self.subtask_groupboxes.remove(gb)
        self.subtask_container_layout.removeWidget(gb)
        gb.deleteLater()

    def save_all_tasks_fun(self, checked):
        logger.info("this button will save all new new tasks")
        logger.debug("prev_task_data: %s", self.prev_task_data)

        subtasks_array = []
        # for index, name_input_lineedit in enumerate(self.module_name_inp_array):
        #     logger.debug("Index: %s || info: %s",index, name_input_lineedit.text()  )

        # for index, description_input_lineedit in enumerate(self.module_description_inp_array):
        #     logger.debug("Index: %s || info: %s",index, description_input_lineedit.text()  )

        # for index, module_status_note_lineedit  in enumerate(self.module_status_note_inp_array):
        #     logger.debug("Index: %s || info: %s",index, module_status_note_lineedit.text()  )
        
        # for index, module_status_item in enumerate(self.module_status_array):
        #     logger.debug("Index: %s || info: %s",index, module_status_item.currentText())


        # using indexing to get all data and append to subtasks_array
        count = 0
        while count < len(self.module_name_inp_array): 
            # get info based on index = count
            # perform validation
            if not self.module_name_inp_array[count].text() or not self.module_description_inp_array[count].text() or not self.module_status_array[count].currentText() or not self.module_status_note_inp_array[count].text():
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Please ensure all fields are field. Check subtasks number {count+1} field name, description, status or status note ",
                    buttons=QMessageBox.StandardButton.Ok
                )
                return 
            
            subtask_dict = {
                "module name": self.module_name_inp_array[count].text().strip(), 
                "module description": self.module_description_inp_array[count].text().strip(), 
                "status": self.module_status_array[count].currentText(), 
                "status note": self.module_status_note_inp_array[count].text().strip(), 
            }
            subtasks_array.append(subtask_dict)
            count+=1


        new_phase = {
            "project":self.project_name,
            "phases": [
                {
                    "phase name": self.phase_name_input.text(),
                    "phase goal": self.phase_goal_input.text(), 
                    "subtasks": subtasks_array
                }
            ]
        }
        logger.debug("new_phase to be added:\n %s",new_phase )

        # appending the previous data
        prev_phases = self.prev_task_data["phases"] # this is an array which holds phases
        logger.debug("type of prev_phases: %s", type(prev_phases))
        for item in new_phase["phases"]: # i need to append new phases to prev_task_data['phases']
            prev_phases.append(item)


        logger.debug("all phases to be added: %s", prev_phases)

        project_tasks = {
            "project":self.project_name,
            "phases": prev_phases 
        }

        logger.debug("Project data: %s", project_tasks)

        operation_result = self.fileManager.update_project_tasks(self.project_name, project_tasks)
        

        if operation_result:  # OK display QMessageBox
            QMessageBox.information(
                self,
                "Success",
                "Task has been added successfully",
                QMessageBox.StandardButton.Ok
            )
            self.phase_name_input.clear()
            self.phase_goal_input.clear()
            self.module_name_input.clear()
            self.module_description_input.clear()
            self.module_status_selector.clear()
            self.module_status_note_input.clear()
        else:
            # Failed QMessageBox
            QMessageBox.warning(
                self,
                "Warning",
                "Project Directory does not exist",
                QMessageBox.StandardButton.Ok
            )

    def closeEvent(self, event):
        self.closed.emit() # emits the signal
        super().closeEvent(event)
    
        

    def exit_window(self, checked):
        logger.debug("Exiting window now")
        self.close() # built  in method that closes the widget


# class TaskApp(QWidget):
#     def __init__(self, userId, newDir):
#         super().__init__()
#         self.userID = userId
#         self.new_dir = newDir

#         # all validation is set in projectPage.py
#         print(f"User ID: {self.userID} : Project Directory: {self.new_dir}")

#         # window layout
#         vapp_layout = QHBoxLayout()

#         # create 2 frames for the window
#         mainFrame = QFrame()
#         sideBarFrame = QFrame()

#         # Sidebar buttons
#         createFlowBtn = QPushButton('Create FlowChart')
#         askAI = QPushButton('Ask AI')
#         exitBtn = QPushButton('Exit')

#         # stying for buttons
#         # createFlowBtn.setStyleSheet("background-color:#e817db;")
#         # askAI.setStyleSheet('background-color:#e817db;  ')
#         # exitBtn.setStyleSheet('background-color:#e817db;  ')

#         sideBarView = QVBoxLayout()  # vertical  layout for the sidebar
#         sideBarView.addWidget(createFlowBtn)
#         sideBarView.addWidget(askAI)
#         sideBarView.addWidget(exitBtn)
#         sideBarView.addStretch(0)
#         sideBarFrame.setLayout(sideBarView)

#         # adding button functionality
#         exitBtn.clicked.connect(self.close_window)

#         deleteTask = QPushButton('Delete')
#         duplicateTask = QPushButton('Duplicate')
#         addTask = QPushButton('Add Tasks')

#         # styling for buttons
#         addTask.setStyleSheet("background-color:green")
#         duplicateTask.setStyleSheet("background-color:green")
#         deleteTask.setStyleSheet("background-color:green")

#         horLayout = QHBoxLayout()  # horizontal button for task management
#         horLayout.addWidget(addTask)
#         horLayout.addWidget(duplicateTask)
#         horLayout.addWidget(deleteTask)

#         # form input for tasks
#         self.taskNumber = 1
#         task_number = QLabel(f'Task Number {self.taskNumber}')

#         # labels
#         name_label = QLabel("Task Name")
#         description_label = QLabel("Task Description")
#         goal_label = QLabel("Goal/Objective: ")

#         # lineedit
#         self.task_name_input = QLineEdit()
#         self.task_description_input = QTextEdit()
#         self.goal_input = QLineEdit()

#         # editting input characteristics
#         # controls the width of the textarea for task description
#         self.task_description_input.setFixedHeight(200)
#         # self.task_description_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
#         # self.task_description_input.setSizePolicy()

#         # buttons for tasks
#         saveBtn = QPushButton('Save')
#         saveBtn.clicked.connect(self.add_task_functionality)

#         # adding to ver_layout form elements
#         ver_layout = QVBoxLayout()
#         ver_layout.addWidget(task_number)
#         ver_layout.addSpacing(10)
#         ver_layout.addWidget(name_label)
#         ver_layout.addWidget(self.task_name_input)
#         ver_layout.addWidget(description_label)
#         ver_layout.addWidget(self.task_description_input)
#         ver_layout.addLayout(horLayout)
#         ver_layout.addWidget(saveBtn)
#         ver_layout.addStretch(0)

#         taskView = QVBoxLayout()
#         taskView.addLayout(ver_layout)

#         mainFrame.setLayout(taskView)
#         vapp_layout.addWidget(sideBarFrame)
#         vapp_layout.addWidget(mainFrame)
#         self.setGeometry(250, 0, 800, 500)
#         self.setLayout(vapp_layout)

#     def add_task_functionality(self):
#         print('project directory:', self.new_dir)
#         # setting project tasks file
#         # /home/alson-kali/PROJECTS/NASA
#         project_dictionary = {
#             "userId": self.userID,
#             "taskNumber": self.taskNumber,
#             "taskName": self.task_name_input.text(),
#             "taskDescription": self.task_description_input.toPlainText(),
#             "userId": self.userID
#         }
#         print("Project Dictionary:")
#         print(project_dictionary)

#         if os.path.exists(self.new_dir):
#             # using writemode||appendmode will create a file
#             projectTaskFilePath = self.new_dir+"/"+"project_task.json"
#             if os.path.exists(projectTaskFilePath) and os.path.getsize(projectTaskFilePath) > 0:
#                 # read file and set data in array
#                 with open(projectTaskFilePath, 'r') as file:
#                     data = json.load(file)
#             else:
#                 data = []  # this ensures if it's first time: data will be an array: writen to file:always read as an array of dictionary

#             data.append(project_dictionary)
#             with open(projectTaskFilePath, 'w') as file:
#                 json.dump(data, file, indent=4)
#             print("Data written to file successfully")
#             QMessageBox.information(
#                 self,
#                 "Success",
#                 "Task has been added successfully",
#                 QMessageBox.StandardButton.Ok
#             )

#         else:
#             print("Project Directory does not exist")
#             QMessageBox.warning(
#                 self,
#                 "Warning",
#                 "Project Directory does not exist",
#                 QMessageBox.StandardButton.Ok
#             )

#     def close_window(self):
#         print("Closing Task Window")
#         self.close()


# app = QApplication()
# window = TaskApp("1234", "~/alson-kali/PROJECTS/taskstrial")
# window.show()
# exit_code = app.exec()
# sys.exit()
