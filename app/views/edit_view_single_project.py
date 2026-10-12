from PySide6.QtWidgets import (
    QApplication, QGraphicsDropShadowEffect, QGroupBox ,QGridLayout, QScrollArea,
    QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QTextEdit
    )
from utils.file_operations import ReadWriteUpdateDeleteFileOperations
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal

from utils.file_operations import ReadWriteUpdateDeleteFileOperations

class EditSingleProjectView(QWidget): 
    closed = Signal() # used to send signal to the parent # used for styling the QStledButton | Other tasks
    # rerun = Signal()
    def __init__(self, projectName):
        super().__init__()
        print("Initiated EditSingleProjectView")
        self.project_name = projectName
        print(f"project_name: {self.project_name}")
        self.setWindowTitle(f"Edit Project: {self.project_name}")
        
        self.project_data = {}

        readWriteUpdateDeleteFileOperationsInstance = ReadWriteUpdateDeleteFileOperations()
        self.project_data = readWriteUpdateDeleteFileOperationsInstance.read_single_project_data(project_name=self.project_name) # returns a project data in dictionary

        appLayout = QVBoxLayout()
        vLayout = QVBoxLayout()
        mywidget = QWidget()
        myScrollArea = QScrollArea()

        def property_styled_label(text):
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:400; font-size:15px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #3A3AC9;')
            return labelStyled
        
        def item_styled_label(text):
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:200; font-size:20px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #2d3748;')
            return labelStyled

        if (self.project_data.__len__ == 0): 
            # set QWidget showing project  file is empty
            print("")
            return
        else:
            item_h_layout = QVBoxLayout()
            item_h_layout.addWidget(property_styled_label('Project Title'))
            item_h_layout.addWidget(QLabel(f'{self.project_data["project_title"]}'))
            item_h_layout.addWidget(property_styled_label('Project Owner'))
            item_h_layout.addWidget(QLabel(f'{self.project_data["project_owner"]}'))
            item_h_layout.addWidget(property_styled_label('Project Status'))
            item_h_layout.addWidget(QLabel(f"{self.project_data['project_status']}"))
            item_h_layout.addWidget(property_styled_label('Project Tags'))
            item_h_layout.addWidget(QLabel(f'{self.project_data["project_tags"]}'))
            item_h_layout.addWidget(property_styled_label('Project Priority'))
            item_h_layout.addWidget(QLabel(f'{self.project_data["project_priority"]}'))
            item_h_layout.addWidget(property_styled_label('Project Description'))
            item_h_layout.addWidget(QTextEdit(f' {self.project_data['project_description']}'))
            item_h_layout.addWidget(property_styled_label('Project Start Date'))
            item_h_layout.addWidget(QLabel(f'{self.project_data["project_start_date"]}'))
            item_h_layout.addWidget(property_styled_label('Project End Date'))
            item_h_layout.addWidget(QLabel(f'{self.project_data["project_end_date"]}'))

            g_row_1 = QGroupBox(self.project_data['project_title'])
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
            g_row_1.setLayout(item_h_layout)
            vLayout.addWidget(g_row_1)
        
        mywidget.setLayout(vLayout)
        myScrollArea.setWidget(mywidget)
        appLayout.addWidget(myScrollArea)
        self.setLayout(appLayout)
        self.setGeometry(200,200, 800,600)

    def closeEvent(self, event):
        print("function to send Signal to parent")
        super().closeEvent(event)