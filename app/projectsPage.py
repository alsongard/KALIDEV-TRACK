from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QTextEdit, QFrame, QDateTimeEdit, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QMessageBox
import sys, os, json
from PySide6.QtCore import QDate


# import class
from createTasks import TaskApp
class ProjectViewAdd(QWidget):
    def __init__(self, userId):
        self.user_id = userId
        super().__init__()

        self.setWindowTitle('Project Page')
        print(f"user_id : {self.user_id}")

        self.user_id = self.user_id.strip("@gmail.com")
        self.newDir = None
        self.task_window = None
        # page view
        appView = QHBoxLayout()

        # create 2 frames
        sideBarFrame = QFrame()
        projectFrame = QFrame()

        # setting the sidebar
        sideBarView = QVBoxLayout()
        createTasks = QPushButton('Create Tasks')
        chatGPTbtn = QPushButton('Ask ChatGPT')
        exitBtn = QPushButton("Exit")


        createTasks.clicked.connect(self.open_project_tasks)
        exitBtn.clicked.connect(self.close_window)
        
        sideBarView.addWidget(createTasks)
        sideBarView.addWidget(chatGPTbtn)
        sideBarView.addWidget(exitBtn)
        sideBarView.addStretch(0)


        exitBtn.clicked.connect(self.close_window)

        # setting up mainProjectView === middle view 
        mainProjectView = QVBoxLayout()
        titleLabel = QLabel('Project Title')
        descriptionLabel = QLabel('Project Description')
        tagLabel = QLabel('Project Tags')
        priorityLabel = QLabel('Project Priority')
        statusLabel = QLabel('Project Status')
        startDateLabel = QLabel('Project Start Date')
        endDateLabel = QLabel('Project End Date')
        ownerLabel = QLabel('Project Owner')


        self.titleInput = QLineEdit()
        self.priorityInput = QLineEdit()
        self.projectTags = QLineEdit()
        self.statusInput = QLineEdit()
        self.ownerInput = QLineEdit()
        self.descriptionInput = QTextEdit()

        # adding functionality to LineEdits
        self.titleInput.setPlaceholderText("Enter Project Title: e.g FreeCodeCamp JS")
        self.statusInput.setPlaceholderText("Enter Project Status: e.g upcoming, delayed, done, in progess")
        self.ownerInput.setPlaceholderText("Enter Project Owner: E.g Your Name")
        self.priorityInput.setPlaceholderText("Enter value betwen 1 to 10")
        self.descriptionInput.setPlaceholderText("Enter Project Description")
        self.projectTags.setPlaceholderText("Enter project Tags: MERN, PySide6 GUI, Game Development")

        ## setting dates for start project time and end project time
        self.start_project_time_edit  = QDateTimeEdit()
        self.end_project_time_edit  = QDateTimeEdit()

        self.start_project_time_edit.setMinimumDate(QDate.currentDate())
        self.end_project_time_edit.setMinimumDate(QDate.currentDate().addDays(7))

        self.start_project_time_edit.setCalendarPopup(True)
        self.end_project_time_edit.setCalendarPopup(True)


        mainProjectView.addWidget(ownerLabel)
        mainProjectView.addWidget(self.ownerInput)
        mainProjectView.addWidget(titleLabel)
        mainProjectView.addWidget(self.titleInput)
        mainProjectView.addWidget(tagLabel)
        mainProjectView.addWidget(self.projectTags)
        mainProjectView.addWidget(descriptionLabel)
        mainProjectView.addWidget(self.descriptionInput)
        mainProjectView.addWidget(statusLabel)
        mainProjectView.addWidget(self.statusInput)
        mainProjectView.addWidget(startDateLabel)
        mainProjectView.addWidget(self.start_project_time_edit)
        mainProjectView.addWidget(endDateLabel)
        mainProjectView.addWidget(self.end_project_time_edit)
        mainProjectView.addWidget(priorityLabel)
        mainProjectView.addWidget(self.priorityInput)


        saveBtn = QPushButton('Save')

        mainProjectView.addWidget(saveBtn)

        # adding functions to button
        saveBtn.clicked.connect(self.save_functionality)

        # adding layouts to frame
        sideBarFrame.setLayout(sideBarView)
        projectFrame.setLayout(mainProjectView)


        appView.addWidget(sideBarFrame)
        appView.addWidget(projectFrame)
        self.setGeometry(200, 0, 800,600)
        self.setLayout(appView)

    def close_window(self):
        print("Closing Window")
        self.close()


    # setting logic for the project Page
    """
    on save what is to be done:
        - create new folder : will have the projects name
        - within the folder save everything to a afile
    """
    def save_functionality(self):
        # get project details
        # after creating the project-title directory we need to get every lineEdit text: method: text()
        title_text  = self.titleInput.text()
        owner_text  = self.ownerInput.text()
        project_tags  = self.projectTags.text()
        description_text  = self.descriptionInput.toPlainText()
        status_text  = self.statusInput.text()
        priority_text = self.priorityInput.text()

        # print()
        user_home_dir = os.path.expanduser("~")
        projectfolder = user_home_dir+"/PROJECTS"
        
        if not os.path.exists(projectfolder):
            os.mkdir(projectfolder)
        
        new_dir = projectfolder+"/"+title_text
        os.mkdir(new_dir)

        self.newDir = new_dir
        # getting project start and end date
        startDateTime = self.start_project_time_edit.dateTime()
        endDateTime = self.end_project_time_edit.dateTime()

   
        startDate = startDateTime.date().toString("yyyy-MM-dd")
        startTime = startDateTime.time().toString("hh-mm AP")

        endDate = endDateTime.date().toString('yyyy-MM-dd')
        endTime = endDateTime.time().toString('hh-mm AP')
        # print("Without to String")
        # print(startDateTime.time())


        saving_message_response = QMessageBox().information(
            self,
            "Information",
            "Project Details will be Saved, Would you like to Proceed? ",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Ok
        )

        if saving_message_response == QMessageBox.StandardButton.Ok:
            print("Proceeding to save project data")
            self.titleInput.clear()
            self.priorityInput.clear()
            self.projectTags.clear()
            self.statusInput.clear()
            self.ownerInput.clear()
            self.descriptionInput.clear()
            project_dictionary = {
                "userId": self.user_id,
                "project_title": title_text,
                "project_owner": owner_text,
                "project_tags": project_tags,
                "project_description": description_text,
                "project_status": status_text,
                "project_priority": priority_text,
                "project_start_date":startDate,
                "project_start_time":startTime,
                "project_end_date":endDate,
                "project_end_time":endTime
            }
            print(project_dictionary)

            # writing data to the file
            file_name =new_dir+"/project_data.json"
            print(file_name)
            with open(file_name, 'a') as file:
                json.dump(project_dictionary, file)

        else:
            QMessageBox().warning(
                self,
                "Warning!",
                "Project Details will not be saved",
                QMessageBox.StandardButton.Ok
            )
    
    def open_project_tasks(self):
        # setting validation for the task window 
        if self.newDir is None or self.user_id is None:
            QMessageBox.critical(
                self,
                "Error",
                "No project directory or user ID specified."
            )
            return
     
        if self.task_window is None:
            self.task_window = TaskApp(self.user_id, self.newDir)
            self.task_window.show()








# app = QApplication()
# window = ProjectView("ffc75283e11d5314c5065a3d7da24748")
# window.show()
# exit_code = app.exec()
# sys.exit(exit_code)





"""

With to String
2025-07-14
Without to String
PySide6.QtCore.QDate(2025, 7, 14
"""