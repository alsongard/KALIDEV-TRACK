import sys
from PySide6.QtWidgets import QApplication ,QLabel, QFrame, QWidget, QGridLayout, QCalendarWidget, QMainWindow, QTextEdit, QToolBar, QStatusBar, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt 



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
        homeButton.setStyleSheet("font-size:30px;")
        settingBtn = QPushButton('Setting')
        fastActionView.addWidget(homeButton)
        fastActionView.addWidget(settingBtn)
        fastActionFrame.setLayout(fastActionView)


        # fastActionView.setStyleSheet('border: 1px solid red')x

        # setting up view 2 
        mainMiddleFrame = QFrame()
        mainMiddleView = QVBoxLayout()
        welcomeLabel = QLabel("Welcome back sir")
        mainMiddleView.addWidget(welcomeLabel)
        kali_pixmap = QPixmap("./assets/icons/kaliDev_canva.png")
        #  Qt::KeepAspectRatio
        kaliDevImg = kali_pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        mainMiddleImage = QLabel()
        mainMiddleImage.setPixmap(kaliDevImg)
        mainMiddleView.addWidget(mainMiddleImage)
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