import sys, json
from PySide6.QtWidgets import QApplication ,QLabel, QFrame, QWidget, QGridLayout, QCalendarWidget, QMainWindow, QTextEdit, QToolBar, QStatusBar, QPushButton, QHBoxLayout, QVBoxLayout, QTableView
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt 
from datetime import datetime

# importing TableModel
from homeTaskTable import TableModel

class TaskAppView(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("KaliDev-Track")

        # we are creating a QMenuBar object() : we are using menuBar() method from QMainWindow()
        menuBarObject = self.menuBar()

        # adding menues to the menuBar
        fileMenuBarMenue = menuBarObject.addMenu("&File")
        editMenuBarMenue = menuBarObject.addMenu("&Edit")
        helpMenuBarMenue = menuBarObject.addMenu("&Help")

        # creating actions|items for the menues objects
        new_file_action = fileMenuBarMenue.addAction('&New')
        new_window_action = fileMenuBarMenue.addAction('&New Window')
        save_file_action = fileMenuBarMenue.addAction('&Save')
        save_as_action = fileMenuBarMenue.addAction('&Save as')
        exit_action = fileMenuBarMenue.addAction('&Exit')

        # setting shortcuts for menuItems/menuActions
        new_file_action.setShortcut("Ctrl+N")
        new_window_action.setShortcut("Ctrl+Shift+N")
        save_file_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut('Ctrl+Shift+S')
        exit_action.setShortcut('Ctrl+Q')

        # creating action|items for edit menue
        undo_action = editMenuBarMenue.addAction('Undo')
        redo_action  = editMenuBarMenue.addAction('Redo')
        cut_action = editMenuBarMenue.addAction('Cut')
        copy_action = editMenuBarMenue.addAction('Copy')
        paste_action = editMenuBarMenue.addAction('Paste')
        find_action = editMenuBarMenue.addAction('Find')
        find_replace_action = editMenuBarMenue.addAction('Find & Replace')

        # setting shortcuts for editAction/Item
        undo_action.setShortcut('Ctrl+U')
        redo_action.setShortcut('Ctrl+R')
        cut_action.setShortcut('Ctrl+X')
        copy_action.setShortcut('Ctrl+C')
        paste_action.setShortcut('Ctrl+X')
        find_action.setShortcut('Ctrl+F')

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
        fastActionFrame  = QFrame()
        fastActionView = QVBoxLayout()
        homeButton = QPushButton("Home")
        # homeButton.setStyleSheet("font-size:30px;")
        settingBtn = QPushButton('Setting')
        fastActionView.addWidget(homeButton)
        fastActionView.addWidget(settingBtn)
        fastActionView.addStretch(0)
        fastActionFrame.setLayout(fastActionView)


        # fastActionView.setStyleSheet('border: 1px solid red')x

        # setting up view 2 
        mainMiddleFrame = QFrame()
        mainMiddleView = QVBoxLayout()
        welcomeLabel = QLabel("Welcome back sir")
        # welcomeLabel.setStyleSheet('border:1px solid red') # testing:
        mainMiddleView.addWidget(welcomeLabel)
        kali_pixmap = QPixmap("./assets/icons/kaliDev_canva.png") 
        #  Qt::KeepAspectRatio
        kaliDevImg = kali_pixmap.scaled(400, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        mainMiddleImage = QLabel()
        # mainMiddleImage.setStyleSheet("border:1px solid red") # testing: 
        mainMiddleImage.setPixmap(kaliDevImg)
        mainMiddleView.addWidget(mainMiddleImage)
        myTasksLabel = QLabel("My Tasks")
        myTasksLabel.setStyleSheet("border:2px solid black; color:white; font-weight: 600; padding:5px;")
        mainMiddleView.addWidget(myTasksLabel)
        myHeaders = ["Task", "Priority","Start Date", "End Date",  "Status", "Warning"]
        
        # how to read data from projects.json
        users_data = [
            ["FreeCodeCamp JavaScript & DataStructures", "10", "2025-07-07", "2025-07-10", "In progress", ""],
            ["KaliDev-Track","10", "2025-07-07", "2025-08-10", "Upcoming", "Red"],
            ["ANN", "10", "2025-07-07", "2025-07-10", "Finished", ""]
        ]
        data = {}
        
        with open("./data/projectData.json", "r") as file:
            data  = json.load(file)
            # print(data)
            # print(type(data))
        

        # converting dates to datetime format
        # date format
        date_format="%Y-%m-%d"
        project_start_date = datetime.strptime(data["project_start_date"], date_format)
        project_end_date = datetime.strptime(data["project_end_date"], date_format)

        # to handle projects in the future we:
        # compare time with now
        today = datetime.now()
        todays_date = today.date() # gives us the date: YY-mm-dd
        print(project_start_date.date() - todays_date)
        if (project_start_date.date() - todays_date).days > 0:
            checking_project_date_comparison = (project_start_date.date() - todays_date).days
            # print('Project is in the future')
            new_user_data = [
                [data["project_title"], data["project_priority"], data["project_start_date"], data["project_end_date"], data["project_status"], 'Future project']
            ]
        else:
            time_left =  abs(project_end_date-project_start_date)
            # print(time_left) # 7 days, 0:00:00
            # print(time_left.days)
            time_left = time_left.days
            print(f"Type : {type(time_left)} and {time_left}")
            myString = str(time_left) + " days"
            # print(myString)
        # project_end_date =datetime.strptime(data["project_"])
            new_user_data = [
                [data["project_title"], data["project_priority"], data["project_start_date"], data["project_end_date"], data["project_status"], myString]
            ]
        # title, priority, startdate, enddate, status, 
        model = TableModel(new_user_data, myHeaders)
        myTable = QTableView()
        myTable.setModel(model)
        myTable.setColumnWidth(0, 316)

        mainMiddleView.addWidget(myTable)

        mainMiddleFrame.setLayout(mainMiddleView)

        # setting up view 3 
        notificationFrame = QFrame()
        notificationView = QVBoxLayout()
        notificatonLabel = QLabel("Notifications")
        notificationView.addWidget(notificatonLabel)
        myCalendar = QCalendarWidget()
        # myCalendar.setGridVisible(True)
        myCalendar.setFixedSize(QSize(250,200))
        notificationView.addWidget(myCalendar)
        upComing_label = QLabel("Upcoming Activities")
        # upComing_label.setStyleSheet("text-align:center")
        notificationView.addWidget(upComing_label)
        notificationView.addStretch(0)
        notificationFrame.setLayout(notificationView)

        # edit the frames
        fastActionFrame.setFrameShape(QFrame.Shape.Box)
        mainMiddleFrame.setFrameShape(QFrame.Shape.Box)
        notificationFrame.setFrameShape(QFrame.Shape.Box)

        gridLayout.addWidget(fastActionFrame, 0, 0)
        gridLayout.addWidget(mainMiddleFrame, 0, 1)
        gridLayout.addWidget(notificationFrame, 0, 2)

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
        self.addToolBar(mainToolBar)

        self.resize(1368,768)
        # self.setGeometry(100,0,1368,768)\



app = QApplication(sys.argv)
window = TaskAppView()
window.show()

exit_code = app.exec()
sys.exit(exit_code)


"""
seting image using QLabel() is a poor choice as when resizing that is using setFixedWidth/Height, 
you don't resize the image but the QLabel() which does affect the aspect ration of the Image
To solve this we use:
```python
QPixmap() # to first load the image
"""