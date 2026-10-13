"""
edit_view_single_project.py

Purpose:
    Provides a View / Edit Window on DelegateButton on HomeTableView
    This View enables the user to modify or view a project tasks

Depends on: 
    - utils.file_operations.ReadWriteUpdateDeleteFileOperations

Exports: 
    EditSingleProjectView

"""
from PySide6.QtWidgets import (
    QApplication, QGraphicsDropShadowEffect, QMessageBox, QGroupBox ,QGridLayout, QScrollArea,
    QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QTextEdit, QLineEdit
    )

from utils.file_operations import ReadWriteUpdateDeleteFileOperations
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal

from utils.file_operations import ReadWriteUpdateDeleteFileOperations

class EditSingleProjectView(QWidget): 
    """
    Setups the view for the editing or viewing a single project tasks

    Attributes:
        self.project_name (string) : the project name which is a sub-directory name in the directory PROJECTS
        self.project_data (dict) : empty dictionary which is used to store the project data 

    Example:
        >>> view = EditSingleProjectView("LizArt")
        >>> view.show()
    """
    closed = Signal() # used to send signal to the parent # used for styling the QStledButton | Other tasks
    # rerun = Signal()
    def __init__(self, projectName):
        super().__init__()
        print("Initiated EditSingleProjectView")
        self.project_name = projectName
        print(f"project_name: {self.project_name}")
        self.setWindowTitle(f"Edit Project: {self.project_name}")
        
        self.project_data = {}

        self.readWriteUpdateDeleteFileOperationsInstance = ReadWriteUpdateDeleteFileOperations()
        self.project_data = self.readWriteUpdateDeleteFileOperationsInstance.read_single_project_data(project_name=self.project_name) # returns a project data in dictionary
        print("this is self.project_data")
        print(self.project_data)
        
        appLayout = QVBoxLayout() # main layout for the Widget window
        vLayout = QVBoxLayout() # vertical layout for the UI components holding project_details e.g Qlabel
        mywidget = QWidget() # widget to be added oto scrollArea
        myScrollArea = QScrollArea() # scrollableArea widget window
        myScrollArea.setWidgetResizable(True)
        buttonLayout = QHBoxLayout()

        saveBtn = QPushButton("save")
        exitBtn = QPushButton("exit")

        buttonLayout.addWidget(saveBtn)
        buttonLayout.addWidget(exitBtn)

        def property_styled_label(text):
            """
            Used for styling QLabel component
            """
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:400; font-size:15px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #3A3AC9;')
            return labelStyled
        
        def item_styled_label(text):
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:200; font-size:20px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #2d3748;')
            return labelStyled

        if (len(self.project_data) == 0): 
            # set QWidget showing project  file is empty
            print(f"Could not find the project data for project: {self.project_name}")
            return
        

        self.user_id = self.project_data["userId"]

        self.project_title_edit = QLineEdit()
        self.project_title_edit.setText(self.project_data["project_title"])

        self.project_owner_edit = QLineEdit()
        self.project_owner_edit.setText(self.project_data["project_owner"])
        
        self.project_tags_edit = QLineEdit()
        self.project_tags_edit.setText(self.project_data["project_tags"])

        self.project_description_edit = QTextEdit()
        self.project_description_edit.setText(self.project_data["project_description"])
        self.project_description_edit.setMinimumWidth(200)
        self.project_status_edit = QLineEdit()
        self.project_status_edit.setText(self.project_data["project_status"])

        self.project_priority_edit = QLineEdit()
        self.project_priority_edit.setText(self.project_data["project_priority"])

        self.project_start_date_edit = QLineEdit()
        self.project_start_date_edit.setText(self.project_data["project_start_date"])

        self.project_start_time_edit = QLineEdit()
        self.project_start_time_edit.setText(self.project_data["project_start_time"])

        self.project_end_date_edit = QLineEdit()
        self.project_end_date_edit.setText(self.project_data["project_end_date"])

        self.project_end_time_edit = QLineEdit()
        self.project_end_time_edit.setText(self.project_data["project_end_time"])

        saveBtn.clicked.connect(self.save_project_tasks_data)
        exitBtn.clicked.connect(self.exit_view)

        item_v_layout = QVBoxLayout()
        
        item_v_layout.addWidget(property_styled_label('Project Title'))
        item_v_layout.addWidget(self.project_title_edit)
        item_v_layout.addWidget(property_styled_label('Project Owner'))
        item_v_layout.addWidget(self.project_owner_edit)
        item_v_layout.addWidget(property_styled_label('Project Status'))
        item_v_layout.addWidget(self.project_status_edit)
        item_v_layout.addWidget(property_styled_label('Project Tags'))
        item_v_layout.addWidget(self.project_tags_edit)
        item_v_layout.addWidget(property_styled_label('Project Priority'))
        item_v_layout.addWidget(self.project_priority_edit)
        item_v_layout.addWidget(property_styled_label('Project Description'))
        item_v_layout.addWidget(self.project_description_edit)
        item_v_layout.addWidget(property_styled_label('Project Start Date'))
        item_v_layout.addWidget(self.project_start_date_edit)
        item_v_layout.addWidget(property_styled_label('Project End Date'))
        item_v_layout.addWidget(self.project_end_date_edit)

        g_row_1 = QGroupBox(self.project_data['project_title'])
        item_v_layout.addLayout(buttonLayout)

        g_row_1.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 18px;
                border: 1px solid #3A3AC9;
                border-radius: 8px;
                margin-top: 12px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                font-size:23px;
            }

            """)
        g_row_1.setLayout(item_v_layout)
        vLayout.addWidget(g_row_1)
        
        mywidget.setLayout(vLayout)
        myScrollArea.setWidget(mywidget)
        appLayout.addWidget(myScrollArea)
        self.setLayout(appLayout)
        self.setGeometry(200,200, 800,600)

    def closeEvent(self, event):
        """
        the closeEvent is a method handler that receives the Qt close event.

        """
        print("function to send Signal to parent")
        self.closed.emit()# emit the close event
        super().closeEvent(event) # this hides the Widget(QWidget) and closes is

    
    def save_project_tasks_data(self):
        print("this will save the project data")
        
        data = {
            "userId" : self.project_data["userId"],
            "project_title" : self.project_title_edit.text(),
            "project_owner" : self.project_owner_edit.text(),
            "project_tags" : self.project_tags_edit.text(),
            "project_description" : self.project_description_edit.toPlainText(),
            "project_status" :  self.project_status_edit.text(),
            "project_priority" : self.project_priority_edit.text(),
            "project_start_date" : self.project_start_date_edit.text(),
            "project_start_time" : self.project_start_time_edit.text(),
            "project_end_date" : self.project_end_date_edit.text(),
            "project_end_time" : self.project_end_time_edit.text()
        }
        print("this is data in save_project_tasks_data")
        print(data)

        operation_result = self.readWriteUpdateDeleteFileOperationsInstance.updateProjectTasks(projectName=self.project_name, data=data)

        if operation_result: # true
            print("result true")
            QMessageBox.information(
                self, 
                "Save",
                "Project Details have been saved",
                buttons=QMessageBox.StandardButton.Ok 
            )
        else: 
            QMessageBox.critical(
                self, 
                "Status: Failed", 
                "Project Details have not been saved!",
                buttons=QMessageBox.StandardButton.Ok
            )

    


    def exit_view(self):
        print("close the view")
        self.close() # built in method for closing the Window
