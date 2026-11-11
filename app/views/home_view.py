"""
home_view.py

Purpose:
	Provides the main landing view for KALIDEV-TRACK
	Displays the main menu which provide functionalities such as help, edit e.t.c
	Displays a table of projects , 2 side bar frames:
		- the fast action side bar: for fast action buttons
		-  the notification bar side bar showcasing calendar, upcoming, completed, pending and active projects

Depends on:
	- models/home_table_model.HomeTableModel
	- views/projects_page_view.ProjectAddView
	- views.view_projects import ViewProjects
	- views.edit_project_view.EditProjectView
	- views.backup_data_view.BackUpProject
	- utils.file_operations.FileManager
	- utils.button_delegate.ButtonDelegate
	- views.edit_view_single_project.EditSingleProjectView
	- views.list_all_projects_view.ListAllProjects
	- views.settings_view.SettingsView
	- views.ask_ai_view.AskAIView
	- views.docs_view.DocsView
	
Exports: 
	HomeAppView
"""

import sys, json
from PySide6.QtWidgets import (
	QApplication, QMessageBox, QItemDelegate,QLabel,QMessageBox ,QFrame, QSizePolicy, QWidget, QGridLayout, QCalendarWidget, 
	QMainWindow, QTextEdit, QToolBar, QStatusBar, QPushButton, QHBoxLayout, QVBoxLayout, QTableView, QComboBox
)
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import QSize, QSortFilterProxyModel
from PySide6.QtCore import Qt
import PySide6.QtCore
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication
import sys
import os

from pydantic import NonNegativeFloat


# importing classes
from app.views.docs_view import DocsView
from models.home_table_model import HomeTableModel
from views.projects_page_view import ProjectAddView
from views.view_projects import ViewProjects
from views.edit_project_view  import EditProjectView
from views.backup_data_view import BackUpProject
from utils.file_operations import  FileManager
from utils.button_delegate import ButtonDelegate 
from views.edit_view_single_project import EditSingleProjectView
from views.list_all_projects_view import ListAllProjects
from views.settings_view import SettingsView
from views.ask_ai_view import AskAIView


import logging
logger = logging.getLogger(__name__)

class HomeAppView(QMainWindow):
	_instance = None
	def __init__(self, username, userID):
		super().__init__()
		self.user = username
		self.usrID = userID
		self.determine_projects_list_to_display = "All"
		self._all_projects = [] # private variable
		self._display_projects = []
		self.fileManagerInstance = FileManager()


		ICON_DIR  = Path(__file__).resolve().parent.parent / "resources"  /"icons"

		# set window title
		self.setWindowTitle("KaliDev-Track")
		self.w = None
		self.project_views = None
		self.project_edit_view = None
		self.sychronize_view = None
		self.help_view =None
		self.task_view = None
		self.ai_assistant_view = None
		self.edit_single_project = None
		self.settings_view = None


		# we are creating a QMenuBar object() : we are using menuBar() method from QMainWindow()
		menuBar = self.menuBar()

		# CREATE MENU FOR menuBar
		file_menu = menuBar.addMenu("&File")
		view_menu = menuBar.addMenu("&View")
		help_menu = menuBar.addMenu("&Help")
		setting_menu = menuBar.addMenu("&Settings")

		# Help menu actions
		documentation_action = QAction("Documentation", self)
		documentation_action.setCheckable(True)

		about_action = QAction("About", self)
		about_action.setCheckable(True)

		documentation_action.setStatusTip("Opens up documentation window")
		documentation_action.triggered.connect(self.open_docs_view)


		# View menu actions
		self.collapse_fastaction_sidebar = QAction("Collapse Fast Actions SideBar", self)
		self.collapse_notification_sidebar = QAction("Collapse Notification Sidebar", self)

		view_menu.addAction(self.collapse_fastaction_sidebar)
		view_menu.addAction(self.collapse_notification_sidebar)
		self.collapse_fastaction_sidebar.triggered.connect(self.toggle_sidebar)
		self.collapse_notification_sidebar.triggered.connect(self.toggle_notification)



		# file menu actions
		self.new_project_action = QAction("New Project", self)
		self.new_project_action.setCheckable(True)
		self.new_project_action.triggered.connect(self.open_new_project_view)
		file_menu.addAction(self.new_project_action)

		self.manage_project_action = QAction("Manage Project", self)
		self.manage_project_action.setCheckable(True)
		self.manage_project_action.triggered.connect(self.open_manage_project_view)
		file_menu.addAction(self.manage_project_action)

		sychronize_action = QAction("Sychronize Project", self)
		sychronize_action.setCheckable(True)
		sychronize_action.triggered.connect(self.open_sychronization_backup_page)
		file_menu.addAction(sychronize_action)

		# exit action
		exit_action = QAction("Exit", self)
		exit_action.setCheckable(True)
		exit_action.triggered.connect(self.close_window)
		file_menu.addAction(exit_action)


		# Setting MENU BAR QACTION
		self.settings_action = QAction("Settings", self)
		self.settings_action.setCheckable(True)
		self.settings_action.triggered.connect(self.open_settings_view)
		setting_menu.addAction(self.settings_action)


		# setting shortcuts for menuItems/menuActions : need to work on shortcuts
		# new_project_action.setShortcut("Ctrl+N")
		# view_project_action.setShortcut("Ctrl+Shift+N")
		# edit_project_action.setShortcut("Ctrl+S")
		# sychronize_project_action.setShortcut('Ctrl+Shift+S')
		# exit_action.setShortcut('Ctrl+Q')

		# creating action|items for edit menue
		# undo_action = setting_menu.addAction('Undo')
		# redo_action  = setting_menu.addAction('Redo')
		# cut_action = setting_menu.addAction('Cut')
		# copy_action = setting_menu.addAction('Copy')
		# paste_action = setting_menu.addAction('Paste')
		# find_action = setting_menu.addAction('Find')
		# find_replace_action = setting_menu.addAction('Find & Replace')

		# setting shortcuts for editAction/Item
		# undo_action.setShortcut('Ctrl+U')
		# redo_action.setShortcut('Ctrl+R')
		# cut_action.setShortcut('Ctrl+X')
		# copy_action.setShortcut('Ctrl+C')
		# paste_action.setShortcut('Ctrl+X')
		# find_action.setShortcut('Ctrl+F')

		# creating action|items for help menue
		help_menu.addAction(about_action)
		help_menu.addAction(documentation_action)

		mainToolBar = QToolBar()
		# self.addToolBar(mainToolBar)
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
		self.homeButton = QPushButton("Home")
		# homeButton.setStyleSheet("font-size:30px;")
		self.settingBtn = QPushButton('Setting')
		self.searchBtn = QPushButton("Search")
		self.newProjectBtn = QPushButton("New Project")
		# self.addTaskBtn = QPushButton("Add Task For Project")
		self.viewProjectBtn = QPushButton("Manage Projects")
		# self.editProjectBtn = QPushButton("Edit Project")
		self.sychronizeBtn = QPushButton("Sychronize")
		self.exitApp = QPushButton("ExitApp")
		self.ai_assistant = QPushButton("AI Assistant")
		self.helpBtn = QPushButton("Help")

		myButtons = [self.settingBtn, self.homeButton, self.searchBtn, self.helpBtn,  self.newProjectBtn,  self.viewProjectBtn, self.sychronizeBtn, self.exitApp, self.ai_assistant]
		for button in myButtons:
			button.setCheckable(True)
			button.setStyleSheet("text-align: left; padding: 5px;")


		self.newProjectBtn.clicked.connect(self.open_new_project_view_fun)
		self.viewProjectBtn.clicked.connect(self.open_view_projects_page)
		self.sychronizeBtn.clicked.connect(self.open_sychronization_backup_page)
		self.settingBtn.clicked.connect(self.open_settings_view)
		self.ai_assistant.clicked.connect(self.open_ai_asistant_view)
		self.exitApp.clicked.connect(self.close_window)
		self.helpBtn.clicked.connect(self.open_docs_view)
		# homeButton.clicked.connect()
		fastActionView.addWidget(self.searchBtn)
		fastActionView.addWidget(self.homeButton)
		fastActionView.addWidget(self.newProjectBtn)
		# fastActionView.addWidget(self.addTaskBtn)
		fastActionView.addWidget(self.viewProjectBtn)
		fastActionView.addWidget(self.ai_assistant)
		# fastActionView.addWidget(self.editProjectBtn)
		fastActionView.addWidget(self.sychronizeBtn )
		fastActionView.addWidget(self.helpBtn)
		fastActionView.addWidget(self.settingBtn)
		fastActionView.addWidget(self.exitApp)
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
		kali_pixmap = QPixmap(str(ICON_DIR/"kaliDev_canva.png")) 
		#  Qt::KeepAspectRatio
		kaliDevImg = kali_pixmap.scaled(300, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
		mainMiddleImage = QLabel()
		# mainMiddleImage.setStyleSheet("border:1px solid red") # testing: 
		mainMiddleImage.setPixmap(kaliDevImg)

		mainMiddleView.addWidget(mainMiddleImage)
		hor_layout = QHBoxLayout()
		myTasksLabel = QLabel("My Projects")
		# hor_layout.setStyleSheet("border:2px solid black; color:white; font-weight: 600; padding:5px;")

		comboBox = QComboBox()
		
		comboBox.addItems(["All", "Completed", "Active", "Overdue", "Future"])
		comboBox.currentTextChanged.connect(self.get_text_changed_combobox)
		hor_layout.addWidget(myTasksLabel)
		hor_layout.addWidget(comboBox)

		mainMiddleView.addLayout(hor_layout)
		myHeaders = ["Task", "Priority","Start Date", "End Date",  "Status", "Action"]
		

		# upcomingActivitiesArray
		self._upcoming_activies = []
		self._passdeadline_activies = []
		self._active_activities = []
		self._completed_activities = []

		# converting dates to datetime format
		# date format
		self._all_projects = self.fileManagerInstance.read_project_directories()


		# print(f"This is self._all_projects")
		# print(self._all_projects)
		# print(len(self._all_projects))
		self._display_projects = []

		if len(self._all_projects) == 0:
			self._display_projects.append(["No Project", "-", "-", "-", "-", "-"])
		else:
			logger.debug("All projects read: %s", len(self._all_projects))
			date_format="%Y-%m-%d" 
			self.apply_filter()
					
					
			# title, priority, startdate, enddate, status, 
			# print(f"self._display_projects : {len(self._display_projects)}")
			# print(self._display_projects)
		logger.debug("All projects in self._display_projects: %s", len(self._display_projects))
		self.model = HomeTableModel(self._display_projects, myHeaders)
		self.proxyModel = QSortFilterProxyModel() # instance of QSortFilterProxyModel, which receives the model
		self.proxyModel.setSourceModel(self.model)

		myTable = QTableView()
		myTable.resizeColumnsToContents()
		myTable.setModel(self.proxyModel)
		button_delegate = ButtonDelegate()
		button_delegate.button_clicked.connect(self.open_single_project_editor)
		myTable.setItemDelegateForColumn(5, button_delegate)
		myTable.setColumnWidth(0, 316)

		mainMiddleView.addWidget(myTable)

		mainMiddleFrame.setLayout(mainMiddleView)

		# setting up view 3 
		# print(f'self._upcoming_activies: {self._upcoming_activies}')
		# print(f'self._passdeadline_activies: {self._passdeadline_activies}')


		self.notificationFrame = QFrame()
		notificationView = QVBoxLayout()
		notificatonLabel = QLabel("Notifications")
		notificationView.addWidget(notificatonLabel)
		myCalendar = QCalendarWidget()
		# myCalendar.setGridVisible(True)
		myCalendar.setFixedSize(QSize(300,200))
		notificationView.addWidget(myCalendar)

		active_label = QLabel("Active Activities")
		active_label.setStyleSheet("color:#2196F3")
		active_label.setMargin(10)
		# modifying the font size
		# font = active_label.font()
		# font.setPointSize(12)
		# active_label.setFont(font)
		active_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
		notificationView.addWidget(active_label)
		index = 1
		for item in self._active_activities:
			active  = QLabel(f"{index}: {item}")
			notificationView.addWidget(active)
			index += 1


		upComing_label = QLabel("Upcoming Activities")
		upComing_label.setStyleSheet("color:#FF9800")
		upComing_label.setMargin(10)
		# font = upComing_label.font()
		# font.setPointSize(10)
		# upComing_label.setFont(font)
		upComing_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
		# upComing_label.setStyleSheet("text-align:center")
		notificationView.addWidget(upComing_label)
		i = 1
		for item in self._upcoming_activies:
			upcoming = QLabel(f"{i}: {item}")
			upcoming.setWordWrap(True)
			notificationView.addWidget(upcoming)
			i += 1


		completedLabel = QLabel("Completed Activies")
		completedLabel.setStyleSheet("color:#09E815;")
		completedLabel.setMargin(5)
		completedLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
		notificationView.addWidget(completedLabel)
		c = 1
		for item in self._completed_activities:
			notificationView.addWidget(QLabel(f"{c}: {item}"))
			c+=1 

		deadlineLabel = QLabel("Passed Deadline")
		deadlineLabel.setStyleSheet("color:#F5293A;")
		deadlineLabel.setMargin(5)
		deadlineLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
		notificationView.addWidget(deadlineLabel)


		# box-shadow:0px 0px 5px blue;: unknown property
		a = 1
		for item in self._passdeadline_activies:
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
			cls._instance = HomeAppView(myName, myId)
		return cls._instance
		# self.setGeometry(100,0,1368,768)\

	def load_projects(self):
		"""
		The  function load_projects is used to read  project_data.json file in PROJECT/projectName directory
		>>> example : PROJECT/KALIDEV-TRACK
		"""
		self._all_projects = self.fileManagerInstance.read_project_directories()
		self.model.update_data(self._all_projects)
		logger.debug("All projects read length: %s", len(self._all_projects))
	

	def apply_filter(self): 
		"""
		Method apply_filter is used to filter projects based on the mode and  the project start and end date
		"""
		logger.debug("Running apply_filter")

		keys = ("project_title", "project_priority", "project_status", "project_start_date", "project_end_date")
		date_format = "%Y-%m-%d"
		mode = self.determine_projects_list_to_display
		logger.debug("selected mode: %s", mode)

		# to handle projects in the future we:
		# compare time with now
		today = datetime.now()
		todays_date = today.date() 
		

		if mode == "All": 
			# filters the project based on date and status and add to self._display_projects
			for project in self._all_projects:
				logger.debug("project: %s", project)
				project_start_date = datetime.strptime(project["project_start_date"], date_format)
				project_end_date = datetime.strptime(project["project_end_date"], date_format)

				# logger.debug("project title: %s", project["project_title"])
				# logger.debug("project_start_date: %s", project_start_date)
				logger.debug("project_end_date: %s", project_end_date)

				# getting the differences between the dates: preferably in days
				# comparing the current date and the deadline: using comparisons < > 
				# logger.debug("todays date: %s", todays_date)
				
				if (project_start_date.date() > todays_date):# future projects
					# logger.debug("project in future")
					self._upcoming_activies.append(project["project_title"])
					self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Future", ""])
				
				elif (project_start_date.date() <= todays_date and project_end_date.date() >= todays_date ):# start with active projects
					logger.debug("project in active")
					self._active_activities.append(project["project_title"])
					self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Active", ""])
				
				elif (project_end_date.date() < todays_date) : # Overdue and Finished projects
					if (project["project_status"].lower() == "completed" or project["project_status"].lower() == "finished"):
						# logger.debug("project completed")
						self._completed_activities.append(project["project_title"])
						self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Completed", ""])
					else:
						# logger.debug("project passed due date")
						self._passdeadline_activies.append(project["project_title"])
						self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Overdue", ""])
		elif mode == "Completed":
			# filters using project status
			logger.debug("Running in mode: %s", self.determine_projects_list_to_display)
			for index, project in enumerate(self._all_projects):
				if project.get("project_status").lower() == "completed" or project.get("project_status").lower() == "finished":
					self._display_projects.append(project)
			
			logger.debug("Completed projects displayed : %s", len(self._display_projects))
			
		elif mode == "Active":
			logger.debug("Running in mode: %s", self.determine_projects_list_to_display)
			# filters using project status  and date
			for index, project in enumerate(self._all_projects):
				project_start_date = datetime.strptime(project["project_start_date"], date_format)
				project_end_date = datetime.strptime(project["project_end_date"], date_format)
				if (project_start_date.date() <= today.date() and project_end_date.date() >= todays_date ):# start with active projects
					self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Active", ""])
			
			logger.debug("Length of displayed projects: %s", len(self._display_projects))
			
		elif mode == "Overdue":
			logger.debug("Running in mode: %s", self.determine_projects_list_to_display)
			# filter using date : project_end_time < today.date
			for index, project in enumerate(self._all_projects):
				project_start_date = datetime.strptime(project["project_start_date"], date_format)
				project_end_date = datetime.strptime(project["project_end_date"], date_format)
				today = datetime.now()
				if (project_end_date.date() < today.date()) : # Overdue projects
					self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Overdue", ""])

			logger.debug("Length of displayed projects: %s", len(self._display_projects))

		elif mode == "Future":
			logger.debug("Running in mode: %s", self.determine_projects_list_to_display)
			# filter using date : project_end_time < today.date
			for index, project in enumerate(self._all_projects):
				project_start_date = datetime.strptime(project["project_start_date"], date_format)
				today = datetime.now()
				if (project_start_date.date() > today.date()):# future projects
					self._display_projects.append([project["project_title"], project["project_priority"],  project["project_start_date"], project["project_end_date"], "Future", ""])
					# foundIndexes(index)

			logger.debug("Length of displayed projects: %s", len(self._display_projects))

		if len(self._display_projects) == 0:
			self._display_projects.append(["No Project", "-", "-", "-", "-", "-"])
		




	def toggle_sidebar(self):
		"""
		Method toggle_sidebar is used to hide and expand the fastActionFrame 
		"""
		if self.fastActionFrameCollapse:
			self.fastActionFrame.setMinimumWidth(0)
			self.fastActionFrame.hide()
			self.fastActionFrameCollapse = False
			self.collapse_fastaction_sidebar.setText("Expand Fast Action Sidebar")
		else:
			self.fastActionFrame.show()
			self.fastActionFrameCollapse = True
			self.collapse_fastaction_sidebar.setText("Collapse Fast Action Sidebar")


	def toggle_notification(self):
		"""
		Method toggle_notification is used to hide or expand the notificationFrame
		"""
		if self.nofication_collapse:
			self.notificationFrame.hide()
			self.nofication_collapse = False
			self.collapse_notification_sidebar.setText("Expand Notification Sidebar")
		else:
			self.notificationFrame.show()
			self.nofication_collapse = True
			self.collapse_notification_sidebar.setText("Collapse Notification Sidebar")


	def open_new_project_view(self, checked):  # using checked to set view
		"""
		Method open_new_project_view is used to open ProjectViewAdd Window (opening new projects)
		"""
		# print("The status for self.w is")
		# print(self.w)
		if checked == True:
			if self.w is  None:
				self.w = ProjectAddView(self.usrID)
				self.w.closed.connect(self.handle_new_project_closed)
				self.w.show()
		else:
			if self.w is not None:
				self.w.close()
				self.w = None

	def handle_new_project_closed(self):
		"""
		Method handle_new_project_closed is a slot for the closed signal from ProjectAddView Class
		"""
		# print("The child widget `is closing : signal received")
		if self.w is not None:
			logger.debug("self.w is not none")
			self.w.close()
			self.w = None
			# self.reload_projects() # this is used to run reload_projects for reading project_data.json files
			self.newProjectBtn.setChecked(False)
			self.new_project_action.setChecked(False)
		
		
	def open_manage_project_view(self, checked):
		if checked == True: # we change using setCheckable(True)
			if self.project_views is None:
				self.project_views = ListAllProjects()
				self.project_views.closed.connect(self.handle_manage_project_view_closed)
				self.project_views.show()
		else: 
			if self.project_views is not None: # an instance exist
				self.project_views.close()
				self.project_views = None

	def handle_manage_project_view_closed(self):
		"""
		Method handle_manage_project_view_closed is used to handle closed signal from ListAllProjects Class
		"""
		logger.debug("Project Views Child Widget is closing : signal received ")
		if self.project_views is not None:
			self.project_views.close()
			self.project_views = None
			self.viewProjectBtn.setChecked(False)
			self.manage_project_action.setChecked(False)


	def open_edit_projects_page(self):
		if self.project_edit_view is None:
			self.project_edit_view = ListAllProjects()
			self.project_edit_view.closed.connect(self.handle_closed_edit_projects_view)
			self.project_edit_view.show()

	def handle_closed_edit_projects_view(self):
		if self.project_edit_view is not None:
			self.project_edit_view.close()
			self.project_edit_view = None


	def open_sychronization_backup_page(self):
		if self.sychronize_view is None:
			self.sychronize_view = BackUpProject(self.user)
			self.sychronize_view.show()


	def reload_projects(self):
		logger.debug("This reloads the reading on projects")
		self.load_projects()

	def open_single_project_editor(self, row):
		"""
		the method open_single_project_editor is connected to the button_delegate QStyleDelegateItem when clicked
		It opens up the edit or view for single project view
		"""
		# print("This will open project view")
		# print(f"Row: {row}")
		name = self.model.myData[row][0]
		# QMessageBox.information(self, "Row clicked", f"You clicked: {name}")
		if self.edit_single_project == None:
			self.edit_single_project = EditSingleProjectView(name)
			self.edit_single_project.closed.connect(self.on_open_single_project_editor_run)
			self.edit_single_project.show()
		else:
			self.edit_single_project.close()
			self.edit_single_project = None
	
	def on_open_single_project_editor_run(self):
		"""
		the method on_open_single_project_editor_run is connected to the EditSingleProjectView closed signal
		which is fired when an instance of the window EditSingleProject View is closed
		"""
		self.edit_single_project= None

	def get_text_changed_combobox(self, text): 
		"""
		the method get_text_changed_combobox is connected to the QComboBox textChanged signal
		"""
		logger.debug("Text Changed: %s", text)
		self.determine_projects_list_to_display = text
			
		if text == "All":
			self.proxyModel.setFilterFixedString("")
		else:
			self.proxyModel.setFilterKeyColumn(4)
			self.proxyModel.setFilterFixedString(text)

		# self.apply_filter()

	def close_window(self):
		logger.debug("Closing the application")
		self.close()
		if self.w is not None:
			self.w.close() # close the project view page
		if self.project_views is not None:
			self.project_views.close() # close the view projects page
		if self.project_edit_view is not None:
			self.project_edit_view.close() # close the edit project page
		if self.sychronize_view is not None:
			self.sychronize_view.close() # close the sychronization backup page
		if self.edit_single_project is not None:
			self.edit_single_project.close()

	
	def open_task_view(self):
		"""
		This function has not been configured yet, but will be used to add tasks to a project
		"""
		logger.debug("will open task_view")


	def open_settings_view(self, checked):
		"""
		Method open_settings_view is used to open  SettingsView window 
		"""
		logger.debug("Running open_settings_view")
		logger.debug("Status of button: %s", checked)
		if checked:
			if self.settings_view is None:
				self.settings_view = SettingsView()
				self.settings_view.closed.connect(self.handle_settings_view_closed)
				self.settings_view.show()
		else:
			if self.settings_view is not None:
				self.settings_view.close()
				self.settings_view = None


	def handle_settings_view_closed(self):
		"""
		Method handle_settings_view_closed is a slot/function for SettingsView closed Signal
		"""
		logger.debug("handle_settings_view_closed executed")
		if self.settings_view is  not None:
			self.settings_view.close()
			self.settings_view = None
			self.settingBtn.setChecked(False)
			self.settings_action.setChecked(False)

	def open_ai_asistant_view(self, checked):
		"""
		Method open_ai_assistant_view is handles opening a AI assistant view

		Args:
			checked(bool): status of button
		"""
		logger.debug("open_ai_assistant_view executed")
		logger.debug("button status: %s", checked)
		logger.debug("Status of self.ai_assistant: %s", self.ai_assistant_view)

		if checked:
			if self.ai_assistant_view is None:
				self.ai_assistant_view = AskAIView()
				self.ai_assistant_view.closed.connect(self.handles_ai_asisstant_view_closed_signal)
				self.ai_assistant_view.show()
			else:
				self.ai_assistant_view.close()
				self.ai_assistant_view = None

	def handles_ai_asisstant_view_closed_signal(self):
		"""
		Method handles_ai_assistant_view_closed_signal is used to handle the closed signal emited by AskAIView class
		"""
		if self.ai_assistant_view is not None:
			self.ai_assistant_view.close()
			self.ai_assistant_view = None

	def open_docs_view(self, checked):
		"""
		Method open_docs_view is used for opening a QWidget window for DocsView class 
		"""
		logger.info("Opening DocsView window")
		if checked:
			if self.help_view is None:
				self.help_view = DocsView()
				self.help_view.show()
		else:
			if self.help_view is not None:
				self.help_view.close()
				self.help_view = None
	
	def handle_help_view_closed_signal(self):
		if self.help_view is not None:
			self.help_view.close()
			self.help_view = None
		


		



		
# app = QApplication(sys.argv)
# window = HomeAppView("alsongadizo@gmail.com","95ee5bad432b214b609b0de351d0df09")
# window.show()
# exit_code = app.exec()
# sys.exit(exit_code)


"""
seting image using QLabel() is a poor choice as when resizing that is using setFixedWidth/Height, 
you don't resize the image but the QLabel() which does affect the aspect ration of the Image
To solve this we use:
```python
QPixmap() # to first load the image
"""