from PySide6.QtWidgets import (
    QApplication, QGraphicsDropShadowEffect, QGroupBox ,QGridLayout, QScrollArea,
    QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QTextEdit
    )
from fileOperations import ReadWriteUpdateDeleteFileOperations
from PySide6.QtGui import QColor
class ViewProjects(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Projects")
        self.setGeometry(100, 100, 600, 400)
        appLayout = QVBoxLayout()
        vLayout = QVBoxLayout()
        gridLayout = QGridLayout()
        mywidget = QWidget()
        myScrollArea = QScrollArea()
        file_data = ReadWriteUpdateDeleteFileOperations().readFiles()
        myScrollArea.setWidgetResizable(True)
        # print(file_data)
        # file_data : array of dictiornaries
        # get the length of file data:
        print(len(file_data))
    

        def property_styled_label(text):
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:400; font-size:15px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #3A3AC9;')
            return labelStyled
        
        def item_styled_label(text):
            labelStyled = QLabel(text)
            labelStyled.setStyleSheet('font-weight:200; font-size:20px; font-family: Verdana, Geneva, Tahoma, sans-serif; color: #2d3748;')
            return labelStyled
        for item in file_data:
            print(item['project_title'])
            item_h_layout = QVBoxLayout()

            # sahdow effect trial:needs research
            # myLabel = QLabel('Project Title:')
            # myLabel.setStyleSheet('font-weight:800; color:#ffffff; padding:10px;')
            # shadow = QGraphicsDropShadowEffect()
            # shadow.setBlurRadius(15)
            # shadow.setOffset(0, 0)
            # shadow.setColor(QColor("#ffffff230"))
            
            # myLabel.setGraphicsEffect(shadow)
            # item_h_layout.addWidget(myLabel)
            item_h_layout.addWidget(property_styled_label('Project Title'))
            item_h_layout.addWidget(QLabel(f' {item["project_title"]}'))
            item_h_layout.addWidget(property_styled_label('Project Owner'))
            item_h_layout.addWidget(QLabel(f'{item["project_owner"]}'))
            item_h_layout.addWidget(property_styled_label('Project Status'))
            item_h_layout.addWidget(QLabel(f"{item['project_status']}"))
            item_h_layout.addWidget(property_styled_label('Project Tags'))
            item_h_layout.addWidget(QLabel(f'{item["project_tags"]}'))
            item_h_layout.addWidget(property_styled_label('Project Priority'))
            item_h_layout.addWidget(QLabel(f'{item["project_priority"]}'))
            item_h_layout.addWidget(property_styled_label('Project Description'))
            item_h_layout.addWidget(QTextEdit(f' {item['project_description']}'))
            item_h_layout.addWidget(property_styled_label('Project Start Date'))
            item_h_layout.addWidget(QLabel(f'{item["project_start_date"]}'))
            item_h_layout.addWidget(property_styled_label('Project End Date'))
            item_h_layout.addWidget(QLabel(f'{item["project_end_date"]}'))
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
            g_row_1.setLayout(item_h_layout)

            # gridLayout.addWidget(QLabel(f'Project Title: {item["project_title"]}'), row, 0)
            # gridLayout.addWidget(QLabel(f'Project Owner: {item["project_owner"]}'), row,1)
            # gridLayout.addWidget(QLabel(f"Project Status: {item['project_status']}"), row,2)
            # gridLayout.addWidget(QLabel(f'Project Tags: {item["project_tags"]}'), row,3)
            # gridLayout.addWidget(QLabel(f'Project Priority: {item["project_priority"]}'), row,4)

            # gridLayout.addWidget(QLabel(f'Project Description : {item['project_description']}'), view_row_1,0)
            # gridLayout.addWidget(QLabel(item['project_start_date']), view_row_2,2)
            # gridLayout.addWidget(QLabel(item['project_end_date']), view_row_2,3)
            # row+=1
            # view_row_1+=1
            # view_row_2+=1
            vLayout.addWidget(g_row_1)
        
        mywidget.setLayout(vLayout)
        myScrollArea.setWidget(mywidget)
        appLayout.addWidget(myScrollArea)
        self.setLayout(appLayout)
        self.setGeometry(200,200, 800,600)



# app = QApplication([])
# window = ViewProjects()
# window.show()
# exit_code = app.exec()