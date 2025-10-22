import sys, json
from PySide6.QtWidgets import QApplication ,QLabel,QMessageBox ,QFrame, QSizePolicy, QWidget, QGridLayout, QCalendarWidget, QMainWindow, QTextEdit, QToolBar, QStatusBar, QPushButton, QHBoxLayout, QVBoxLayout, QTableView
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
import PySide6.QtCore
from datetime import datetime

# importing class
from homeTaskTable import TableModel
from fileOperations import ReadWriteUpdateDeleteFileOperations
from projectsPage import ProjectViewAdd
from viewProjects import ViewProjects
from editProjectDetails  import EditProjectView
from backupDataView import BackUpProject
import os
class TaskAppView(QMainWindow):
    _instance = None
    def __init__(self, username, userID):
        self.user = username
        self.usrID = userID
        super().__init__()

        # set window title
        self.setWindowTitle("KaliDev-Track")
        self.w = None
        self.project_views = None
        self.project_edit_view = None
        self.sychronize_view = None
        # we are creating a QMenuBar object() : we are using menuBar() method from QMainWindow()
        menuBarObject = self.menuBar()

        # adding menues to the menuBar
        fileMenuBarMenue = menuBarObject.addMenu("&File")
        # editMenuBarMenue = menuBarObject.addMenu("&Edit")
        helpMenuBarMenue = menuBarObject.addMenu("&Help")
        viewMenuBarMenue = menuBarObject.addMenu("&View")

        
        # viewMenuBareMenueItems/Action
        collapse_action = viewMenuBarMenue.addAction("Collapse SideBar")
        notification_action = viewMenuBarMenue.addAction("Collapse Notification")
        collapse_action.triggered.connect(self.toggle_sidebar)
        notification_action.triggered.connect(self.toggle_notification)
        # actions for menuBar
        # collapseAction = QAction("Collapse", self)
        # collapseAction.triggered.connect(self.toggle_sidebar)
        # collapseActionMenuBarMenue.addAction(collapseAction)


        # creating actions|items for the menues objects
        new_project_action = fileMenuBarMenue.addAction('&New Project')
        view_project_action = fileMenuBarMenue.addAction('&View Projects')
        edit_project_action = fileMenuBarMenue.addAction('&Edit Project')
        sychronize_project_action = fileMenuBarMenue.addAction('&Sychronize Project')
        exit_action = fileMenuBarMenue.addAction('&Exit')

        new_project_action.triggered.connect(self.open_project_page)
        view_project_action.triggered.connect(self.open_view_projects_page)
        edit_project_action.triggered.connect(self.open_edit_projects_page)
        sychronize_project_action.triggered.connect(self.open_sychronization_backup_page)
        exit_action.triggered.connect(self.close_window)



        # setting shortcuts for menuItems/menuActions : need to work on shortcuts
        # new_project_action.setShortcut("Ctrl+N")
        # view_project_action.setShortcut("Ctrl+Shift+N")
        # edit_project_action.setShortcut("Ctrl+S")
        # sychronize_project_action.setShortcut('Ctrl+Shift+S')
        # exit_action.setShortcut('Ctrl+Q')

        # creating action|items for edit menue
        # undo_action = editMenuBarMenue.addAction('Undo')
        # redo_action  = editMenuBarMenue.addAction('Redo')
        # cut_action = editMenuBarMenue.addAction('Cut')
        # copy_action = editMenuBarMenue.addAction('Copy')
        # paste_action = editMenuBarMenue.addAction('Paste')
        # find_action = editMenuBarMenue.addAction('Find')
        # find_replace_action = editMenuBarMenue.addAction('Find & Replace')

        # setting shortcuts for editAction/Item
        # undo_action.setShortcut('Ctrl+U')
        # redo_action.setShortcut('Ctrl+R')
        # cut_action.setShortcut('Ctrl+X')
        # copy_action.setShortcut('Ctrl+C')
        # paste_action.setShortcut('Ctrl+X')
        # find_action.setShortcut('Ctrl+F')

        # creating action|items for help menue
        helpMenuBarMenue.addAction('About')
        helpMenuBarMenue.addAction('Documentation')

        mainToolBar = QToolBar()
        mainToolBar.setIconSize(QSize(20, 20))



        new_fileToolBarItem = QAction(QIcon("./assets/icons/new_File_icon.png"), "New", self)
        new_fileToolBarItem.setStatusTip('New file')

        save_fileToolBarItem = QAction(QIcon("./assets/icons/save_File_Icon.jpeg"), "Save", self)
        save_fileToolBarItem.setStatusTip('Save')

        redo_fileToolBarItem = QAction(QIcon("./assets/icons/redo_icon.png"), "Redo", self)
        redo_fileToolBarItem.setStatusTip('Redo')

        undo_fileToolBarItem = QAction(QIcon("./assets/icons/undo_icon_copy.png"), "Undo", self)
        undo_fileToolBarItem.setStatusTip('Undo')

        copy_ToolBarItem = QAction(QIcon("./assets/icons/copy_icon.png"), "Copy", self)
        copy_ToolBarItem.setStatusTip('Copy')

        cut_ToolBarItem = QAction(QIcon("./assets/icons/cut_copy.png"), "Cut", self)
        cut_ToolBarItem.setStatusTip("Cut")



        mainToolBar.addAction(new_fileToolBarItem)
        mainToolBar.addAction(save_fileToolBarItem)
        mainToolBar.addAction(redo_fileToolBarItem)
        mainToolBar.addAction(undo_fileToolBarItem)
        mainToolBar.addAction(copy_ToolBarItem)
        mainToolBar.addAction(cut_ToolBarItem)

        gridLayout = QGridLayout()
        """
        the gridLayout must have 1 row and 3 columns
        the 3 columns are as follows
        1: fast action buttons: access
        2: main central view/widget
        3: calendar, notifications
        """

        # setting up view 1
        self.fastActionFrame  = QFrame()
        # F0F0F4
        self.fastActionFrame.setStyleSheet("background-color:#0B0B0F;")
        # self.fastActionFrame.setStyleSheet("background-image:linear-gradient:(to right, blue, black);")
        fastActionView = QVBoxLayout()
        homeButton = QPushButton("Home")
        # homeButton.setStyleSheet("font-size:30px;")
        settingBtn = QPushButton('Setting')
        searchBtn = QPushButton("Search")
        newProjectBtn = QPushButton("New Project")
        viewProjectBtn = QPushButton("View Projects")
        editProjectBtn = QPushButton("Edit Project")
        sychronizeBtn = QPushButton("Sychronize")
        exitApp = QPushButton("ExitApp")


        newProjectBtn.clicked.connect(self.open_project_page)
        viewProjectBtn.clicked.connect(self.open_view_projects_page)
        editProjectBtn.clicked.connect(self.open_edit_projects_page)
        sychronizeBtn.clicked.connect(self.open_sychronization_backup_page)
        exitApp.clicked.connect(self.close_window)
        # homeButton.clicked.connect()
        fastActionView.addWidget(searchBtn)
        fastActionView.addWidget(homeButton)
        fastActionView.addWidget(newProjectBtn)
        fastActionView.addWidget(viewProjectBtn)
        fastActionView.addWidget(editProjectBtn)
        fastActionView.addWidget(sychronizeBtn )
        fastActionView.addWidget(settingBtn)
        fastActionView.addWidget(exitApp)
        fastActionView.addStretch(0)
        self.fastActionFrame.setLayout(fastActionView)
        self.fastActionFrameCollapse = True
        # self.fastActionFrame.

        # fastActionView.setStyleSheet('border: 1px solid red')x

        # setting up view 2 
        mainMiddleFrame = QFrame()
        mainMiddleFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        mainMiddleView = QVBoxLayout()
        welcomeLabel = QLabel(f"Welcome back {self.user}")
        # welcomeLabel.setStyleSheet('border:1px solid red') # testing:
        mainMiddleView.addWidget(welcomeLabel)
        kali_pixmap = QPixmap("./assets/icons/kaliDev_canva.png") 
        #  Qt::KeepAspectRatio
        kaliDevImg = kali_pixmap.scaled(300, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        mainMiddleImage = QLabel()
        # mainMiddleImage.setStyleSheet("border:1px solid red") # testing: 
        mainMiddleImage.setPixmap(kaliDevImg)

        mainMiddleView.addWidget(mainMiddleImage)
        myTasksLabel = QLabel("My Tasks")
        myTasksLabel.setStyleSheet("border:2px solid black; color:white; font-weight: 600; padding:5px;")
        mainMiddleView.addWidget(myTasksLabel)
        myHeaders = ["Task", "Priority","Start Date", "End Date",  "Status", "Warning"]
        

        # upcomingActivitiesArray
        upcomingActivites = []
        passDeadlineActivities = []

        # how to read data from projects.json
        with open("./data/projectData.json", "r") as file:
            data  = json.load(file)
            # print(data)
            # print(type(data))
        

        # converting dates to datetime format
        # date format
        read_instance = ReadWriteUpdateDeleteFileOperations()
        geazy = read_instance.readFiles()
        # print(f"This is geazy")
        # print(geazy)
        # print(len(geazy))
        new_user_data = []

        if len(geazy) == 0:
            new_user_data.append(["No Project", "-", "-", "-", "-", "-"])
            # since we know the path does not exist we need to create the folder
            value = read_instance.createProjectFolder()
            if value == 0:
                QMessageBox.information(
                    self,
                    "INformation",
                    "Your New Project folder has been created at: ~/PROJECTS",
                    QMessageBox.StandardButton.Ok 
                )
        else:
            date_format="%Y-%m-%d" 
            for item  in geazy:
                # print('this is dictionary')
                # print(item) # item is dictionary
                # print(item)
                project_start_date = datetime.strptime(item["project_start_date"], date_format)
                project_end_date = datetime.strptime(item["project_end_date"], date_format)

                print(f"project_start_date: {project_start_date.date()} ")
                print(f"project_end_date: {project_end_date.date()}")


                # getting the differences between the dates: preferably in days
                # comparing the current date and the deadline: using comparisons < > 
                current_date = datetime.now()
                
                # to handle projects in the future we:
                # compare time with now
                today = datetime.now()
                todays_date = today.date() # gives us the date: YY-mm-dd
                # print(f'{item["project_title"]}: days subtraction')
                # print(todays_date)

                if project_end_date.date() > todays_date: 
                    # if in future
                    # print(f"Project in the future: {item['project_title']}") # testing: working
                    checking_project_date_comparison = (project_start_date.date() - todays_date).days
                    new_user_data.append([item["project_title"], item["project_priority"], item["project_start_date"], item["project_end_date"], "Future", 'Future project'])
                    upcomingActivites.append(item["project_title"])
                else:
                    # print(f"Project in the past: {item['project_title']}") # testing: working
                    time_left = todays_date - project_end_date.date()
                    # print("time_left") # testing: working
                    # print(time_left) # testing: working
                    time_left = time_left.days
                    # print(f"Type : {type(time_left)} and {time_left}")
                    myString = str(time_left) + " days"
                    passDeadlineActivities.append(item["project_title"])
                    new_user_data.append([item["project_title"], item["project_priority"], item["project_start_date"], item["project_end_date"], "Passed Deadline", myString])

                    # title, priority, startdate, enddate, status, 
            # print(f"new_user_data")
            # print(new_user_data)
        model = TableModel(new_user_data, myHeaders)
        myTable = QTableView()
        myTable.setModel(model)
        myTable.setColumnWidth(0, 316)

        mainMiddleView.addWidget(myTable)

        mainMiddleFrame.setLayout(mainMiddleView)

        # setting up view 3 
        # print(f'upcomingActivites: {upcomingActivites}')
        # print(f'passDeadlineActivities: {passDeadlineActivities}')


        self.notificationFrame = QFrame()
        notificationView = QVBoxLayout()
        notificatonLabel = QLabel("Notifications")
        notificationView.addWidget(notificatonLabel)
        myCalendar = QCalendarWidget()
        # myCalendar.setGridVisible(True)
        myCalendar.setFixedSize(QSize(300,200))
        notificationView.addWidget(myCalendar)
        upComing_label = QLabel("Upcoming Activities")
        upComing_label.setStyleSheet("color:#4B2EEF")
        upComing_label.setMargin(10)
        upComing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # upComing_label.setStyleSheet("text-align:center")
        notificationView.addWidget(upComing_label)
        i = 1
        for item in upcomingActivites:
            upcoming = QLabel(f"{i}: {item}")
            upcoming.setWordWrap(True)
            notificationView.addWidget(upcoming)
            i += 1

        deadlineLabel = QLabel("Passed Deadline")
        deadlineLabel.setStyleSheet("color:#F5293A;")
        deadlineLabel.setMargin(5)
        deadlineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notificationView.addWidget(deadlineLabel)


        # box-shadow:0px 0px 5px blue;: unknown property
        a = 1
        for item in passDeadlineActivities:
            notificationView.addWidget(QLabel(f"{a}: {item}"))
            a+=1

        notificationView.addStretch(0)
        self.notificationFrame.setLayout(notificationView)

        # edit the frames
        self.fastActionFrame.setFrameShape(QFrame.Shape.Box)
        mainMiddleFrame.setFrameShape(QFrame.Shape.Box)
        self.notificationFrame.setFrameShape(QFrame.Shape.Box)
        self.nofication_collapse = True

        gridLayout.addWidget(self.fastActionFrame, 0, 0)
        gridLayout.addWidget(mainMiddleFrame, 0, 1)
        gridLayout.addWidget(self.notificationFrame, 0, 2)

        # setting the width for the columns
        gridLayout.setColumnMinimumWidth(0, 200)
        gridLayout.setColumnStretch(1, 2)
        gridLayout.setColumnMinimumWidth(1, 400)
        gridLayout.setColumnMinimumWidth(2, 200)
        
        mainWidget = QWidget()
        mainWidget.setLayout(gridLayout)
        # taskView = QVBoxLayout()
        # taskView.addLayout(gridLayout)

        self.setCentralWidget(mainWidget)
        # self.addToolBar(mainToolBar) # future:uncomment to set functionality for toolBar

        self.resize(1368,768)

    @classmethod
    def get_instance(cls,myName, myId, parent=None):
        if cls._instance is None:
            cls._instance = TaskAppView(myName, myId)
        return cls._instance
        # self.setGeometry(100,0,1368,768)\


    def toggle_sidebar(self):
        if self.fastActionFrameCollapse:
            self.fastActionFrame.setMinimumWidth(0)
            self.fastActionFrame.hide()
            self.fastActionFrameCollapse = False

        else:
            self.fastActionFrame.show()
            self.fastActionFrameCollapse = True

    def toggle_notification(self):
        if self.nofication_collapse:
            self.notificationFrame.hide()
            self.nofication_collapse = False
        else:
            self.notificationFrame.show()
            self.nofication_collapse = True

    def open_project_page(self):
        if self.w is  None:
            self.w = ProjectViewAdd(self.usrID)
            self.w.show()

    def open_view_projects_page(self):
        if self.project_views is None:
            self.project_views = ViewProjects()
            self.project_views.show()

    def open_edit_projects_page(self):
        if self.project_edit_view is None:
            self.project_edit_view = EditProjectView()
            self.project_edit_view.show()

    def open_sychronization_backup_page(self):
        if self.sychronize_view is None:
            self.sychronize_view = BackUpProject(self.user)
            self.sychronize_view.show()

    def close_window(self):
        print("Closing the application")
        self.close()
        if self.w is not None:
            self.w.close() # close the project view page
        if self.project_views is not None:
            self.project_views.close() # close the view projects page
        if self.project_edit_view is not None:
            self.project_edit_view.close() # close the edit project page
        if self.sychronize_view is not None:
            self.sychronize_view.close() # close the sychronization backup page

app = QApplication(sys.argv)
window = TaskAppView("Alson-Kali","55d345c42a160d35e4acb949bb711608")
# window.show()
exit_code = app.exec()
sys.exit(exit_code)


"""
seting image using QLabel() is a poor choice as when resizing that is using setFixedWidth/Height, 
you don't resize the image but the QLabel() which does affect the aspect ration of the Image
To solve this we use:
```python
QPixmap() # to first load the image
"""