"""
backup_data_view.py

Purpose:
    Provides a view for backing up projects phases / tasks into storage service provider e.g mongodb


Exports:
    BackUpProject
"""


from PySide6.QtWidgets import (
    QApplication, QGraphicsDropShadowEffect, QGroupBox ,QGridLayout, QScrollArea,QMessageBox,
    QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QTextEdit
    )
from PySide6.QtGui import QColor
import os, json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.file_operations import ReadWriteUpdateDeleteFileOperations
from dotenv import load_dotenv 

class BackUpProject(QWidget):
    """
    Provides a QWidget window for which the user can backup projects into storage provide

    Attributes:
        self.username (string): the username for the user logged in 
        self.connect_status (boolean) : indicates status of connection to online storage service

    """
    def __init__(self, user):
        """
        Configure  a view window which is used to setup the view for the user

        """
        super().__init__()
        self.username = user
        self.setWindowTitle("View Projects")
        self.setGeometry(100, 100, 600, 400)
        appLayout = QVBoxLayout() # the main layout used for this QWidget
        vLayout = QVBoxLayout() # tthe vertical layout which holds the GroupBox Instances(which provide UI components for each project)
        gridLayout = QGridLayout()
        load_dotenv()
        mywidget = QWidget()
        myScrollArea = QScrollArea()
        myScrollArea.setWidgetResizable(True)
        # print(f'This is mongoURI: {os.getenv("MONGO_URI")}') // working success
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.connect_status = None
        print(f'username: {self.username}')
        try:
            self.client.admin.command('ping')
            print("Connection Successfull")
            QMessageBox.information(
                self,
                "Information",
                "Connection to MongoDB is successful.",
                QMessageBox.StandardButton.Ok
            )
            self.connect_status = True
        except ConnectionFailure:
            print('Connection to database failed!')
            QMessageBox.critical(
                self,
                "Error",
                "Connection to MongoDB failed. Check Documentation for more help",
                QMessageBox.StandardButton.Ok
            )

        file_data = ReadWriteUpdateDeleteFileOperations().readFiles()

        print(len(file_data))

        home_dir = os.path.expanduser("~")
        self.app_project_folder = home_dir+"/"+"PROJECTS"

        def property_styled_label(text):
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:400; font-size:15px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #3A3AC9;')
            return labelStyled
        

        for item in file_data:
            print(item['project_title'])
            title=item['project_title']
            print(f'Title: {title}')
            item_v_layout = QVBoxLayout() # vertical layout for the individual labels for the project
            buttonLayout = QHBoxLayout() # button layout
            backUpBtn = QPushButton("BackUp Project") # backUpBtn
            comparePrjctDetails = QPushButton("Sychronize Project details")

            # adding functionality to the button
            backUpBtn.clicked.connect(lambda checked, t=title: self.backUp_project(t))

            buttonLayout.addWidget(backUpBtn)
            buttonLayout.addWidget(comparePrjctDetails)
            item_v_layout.addWidget(property_styled_label('Project Title'))
            item_v_layout.addWidget(QLabel(f' {item["project_title"]}'))
            item_v_layout.addWidget(property_styled_label('Project Owner'))
            item_v_layout.addWidget(QLabel(f'{item["project_owner"]}'))
            item_v_layout.addWidget(property_styled_label('Project Status'))
            item_v_layout.addWidget(QLabel(f"{item['project_status']}"))
            item_v_layout.addWidget(property_styled_label('Project Tags'))
            item_v_layout.addWidget(QLabel(f'{item["project_tags"]}'))
            item_v_layout.addWidget(property_styled_label('Project Priority'))
            item_v_layout.addWidget(QLabel(f'{item["project_priority"]}'))

            item_v_layout.addLayout(buttonLayout)
            g_row_1 = QGroupBox(item['project_title'])
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

    def backUp_project(self, title):
        """
        Backups up project data to storage provider
        

        Args:
            title (string): This is the title of the project, which is the name used to create the  sub-directory name for the project

        
        Return:
            None
        """
        print(f'Backuped project is : {title}')
        project_path = self.app_project_folder+"/"+title
        if os.path.exists(project_path):
            data_file = project_path+"/"+"project_data.json"
            print(data_file)
            with open(data_file, "r") as file:
                project_data = json.load(file)
                print(f'this is project data: \n {project_data}')
            if self.connect_status:
                userProjectDetailsDB = self.client[self.username]
                userCollection = userProjectDetailsDB[f'{self.username}ProjectDetails']
                record_added = userCollection.insert_one(project_data)
                print(record_added)
                if record_added.acknowledged: # check it's true
                    QMessageBox.information(
                        self,
                        "Information",
                        "Project data has been backed up successfully.",
                        QMessageBox.StandardButton.Ok
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Failed to back up project data.",
                        QMessageBox.StandardButton.Ok
                    )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Connection to MongoDB is not established! Cannot BackUp Data.",
                    QMessageBox.StandardButton.Ok
                )

        else:
            print("no filepath exist")
            QMessageBox.critical(
                self,
                "Error",
                "Project path does not exist.",
                QMessageBox.StandardButton.Ok
            )



# app = QApplication([])
# window = BackUpProject("jupiter")
# window.show()
# exit_code = app.exec()