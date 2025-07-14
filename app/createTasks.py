from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy, QPushButton, QLabel, QLineEdit, QTextEdit, QFrame, QVBoxLayout, QHBoxLayout
import sys
class TaskApp(QWidget):
    def __init__(self):
        super().__init__()

        # window layout
        vapp_layout = QHBoxLayout()

        # create 2 frames for the window
        mainFrame = QFrame()
        sideBarFrame = QFrame()
        createFlowBtn = QPushButton('Create FlowChart')
        chatGptBtn  = QPushButton('Ask ChatGpt')


        # stying for buttons
        createFlowBtn.setStyleSheet("background-color:#e817db;")
        chatGptBtn.setStyleSheet('background-color:#e817db;  ')
        sideBarView = QVBoxLayout()
        sideBarView.addWidget(createFlowBtn)
        sideBarView.addWidget(chatGptBtn)
        sideBarView.addStretch(0)
        sideBarFrame.setLayout(sideBarView)

       
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
        task_name_input = QLineEdit()
        description_label = QLabel("Task Description")
        task_description_input = QTextEdit()

        # editting input characteristics
        task_description_input.setFixedHeight(200)
        # task_description_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # task_description_input.setSizePolicy()

        # buttons for tasks
        saveBtn = QPushButton('Save')


        # adding to ver_layout form elements
        ver_layout = QVBoxLayout()
        ver_layout.addWidget(task_number)
        ver_layout.addSpacing(10)
        ver_layout.addWidget(name_label)
        ver_layout.addWidget(task_name_input)
        ver_layout.addWidget(description_label)
        ver_layout.addWidget(task_description_input)
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
        pass


app = QApplication()
window = TaskApp()
window.show()
exit_code = app.exec()
sys.exit()