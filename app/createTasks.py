from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QSizePolicy, QPushButton, QLabel, QLineEdit, QTextEdit, QFrame, QVBoxLayout, QHBoxLayout
import sys, os, json

class TaskApp(QWidget):
    def __init__(self, userId, newDir):
        super().__init__()
        self.userID = userId
        self.new_dir = newDir

        # all validation is set in projectPage.py
        print(f"User ID: {self.userID} : Project Directory: {self.new_dir}")



        # window layout
        vapp_layout = QHBoxLayout()

        # create 2 frames for the window
        mainFrame = QFrame()
        sideBarFrame = QFrame()
        createFlowBtn = QPushButton('Create FlowChart')
        chatGptBtn  = QPushButton('Ask ChatGpt')
        exitBtn = QPushButton('Exit')


        # stying for buttons
        createFlowBtn.setStyleSheet("background-color:#e817db;")
        chatGptBtn.setStyleSheet('background-color:#e817db;  ')
        exitBtn.setStyleSheet('background-color:#e817db;  ')
        sideBarView = QVBoxLayout()
        sideBarView.addWidget(createFlowBtn)
        sideBarView.addWidget(chatGptBtn)
        sideBarView.addWidget(exitBtn)
        sideBarView.addStretch(0)
        sideBarFrame.setLayout(sideBarView)


        # adding button functionality
        exitBtn.clicked.connect(self.close_window)

       
        deleteTask = QPushButton('Delete')
        duplicateTask = QPushButton('Duplicate')
        addTask = QPushButton('Add Tasks')

        # styling for buttons
        addTask.setStyleSheet("background-color:green")
        duplicateTask.setStyleSheet("background-color:green")
        deleteTask.setStyleSheet("background-color:green")

        horLayout = QHBoxLayout()
        horLayout.addWidget(addTask)
        horLayout.addWidget(duplicateTask)
        horLayout.addWidget(deleteTask)


        # form input for tasks
        self.taskNumber = 1
        task_number = QLabel(f'Task Number {self.taskNumber}')
        name_label = QLabel("Task Name")
        self.task_name_input = QLineEdit()
        description_label = QLabel("Task Description")
        self.task_description_input = QTextEdit()

        # editting input characteristics
        self.task_description_input.setFixedHeight(200)
        # self.task_description_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.task_description_input.setSizePolicy()

        # buttons for tasks
        saveBtn = QPushButton('Save')
        saveBtn.clicked.connect(self.add_task_functionality)


        # adding to ver_layout form elements
        ver_layout = QVBoxLayout()
        ver_layout.addWidget(task_number)
        ver_layout.addSpacing(10)
        ver_layout.addWidget(name_label)
        ver_layout.addWidget(self.task_name_input)
        ver_layout.addWidget(description_label)
        ver_layout.addWidget(self.task_description_input)
        ver_layout.addLayout(horLayout)
        ver_layout.addWidget(saveBtn)
        ver_layout.addStretch(0)



        taskView = QVBoxLayout()
        taskView.addLayout(ver_layout)

        mainFrame.setLayout(taskView)
        vapp_layout.addWidget(sideBarFrame)
        vapp_layout.addWidget(mainFrame)
        self.setGeometry(250,0, 800,500)
        self.setLayout(vapp_layout)

    def add_task_functionality(self):
        print('project directory:', self.new_dir)
        # setting project tasks file
        # /home/alson-kali/PROJECTS/NASA
        project_dictionary = {
            "userId": self.userID,
            "taskNumber": self.taskNumber,
            "taskName": self.task_name_input.text(),
            "taskDescription": self.task_description_input.toPlainText(),
            "userId": self.userID
        }
        print("Project Dictionary:")
        print(project_dictionary)


        if os.path.exists(self.new_dir):
            # using writemode||appendmode will create a file
            projectTaskFilePath = self.new_dir+"/"+"project_task.json"
            if os.path.exists(projectTaskFilePath) and os.path.getsize(projectTaskFilePath) > 0:
                # read file and set data in array
                with open(projectTaskFilePath, 'r') as file:
                    data = json.load(file)
            else:
                data = [] # this ensures if it's first time: data will be an array: writen to file:always read as an array of dictionary

            data.append(project_dictionary)
            with open(projectTaskFilePath, 'w') as file:
                json.dump(data, file, indent=4)
            print("Data written to file successfully")
            QMessageBox.information(
                self,
                "Success",
                "Task has been added successfully",
                QMessageBox.StandardButton.Ok
            )

        else:
            print("Project Directory does not exist")
            QMessageBox.warning(
                self,
                "Warning",
                "Project Directory does not exist",
                QMessageBox.StandardButton.Ok
            )
    def close_window(self):
        print("Closing Task Window")
        self.close()

# app = QApplication()
# window = TaskApp()
# window.show()
# exit_code = app.exec()
# sys.exit()