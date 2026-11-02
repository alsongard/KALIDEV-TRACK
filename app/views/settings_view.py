"""
settings_view.py

Purpose: 
    Provides the SettingsView class, which is a QWidget that represents the settings view in the application. 
    This view allows users to configure various settings related to the application.
"""
from PySide6.QtCore import QCborMap, QLine
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QPushButton, QWidget, QComboBox, QGroupBox, QVBoxLayout, QLabel

class SettingsView(QWidget):
    """
    A QWidget that represents the settings view in the application.
    """

    def __init__(self): 
        """
        Class constructor method
        """
        super().__init__()
     

        self.main_layout = QVBoxLayout() 
        self.containter = QGroupBox()
        container_layout= QVBoxLayout()

        title_save_layout = QHBoxLayout()
        title_label = QLabel("Settings")
        title_label.setStyleSheet("font-weight:bold; font-size:18px")
        saveBtn = QPushButton("Save")
        title_save_layout.addWidget(title_label)
        title_save_layout.addWidget(saveBtn)

        description_label = QLabel("Configure settings for your application")

        self.main_layout.addLayout(title_save_layout)
        self.main_layout.addWidget(description_label)

        # dark_mode_layout = QHBoxLayout()
        dark_mode_settings= QComboBox()
        dark_label = QLabel("Dark Mode Settings")
        dark_mode_settings.addItems(["True", "False"])

        container_layout.addWidget(dark_label)
        container_layout.addWidget(dark_mode_settings)



        email_label = QLabel("Enter email used for notifications: ")
        self.email_for_notification = QLineEdit()
        self.email_for_notification.setPlaceholderText("Set email for notification")

        container_layout.addWidget(email_label)
        container_layout.addWidget(self.email_for_notification)

        # save_data_config_layout = QHBoxLayout()
        save_data_label=QLabel("Save data before exiting: ")
        save_data_option = QComboBox()
        save_data_option.addItems(["True", "False"])
        
        container_layout.addWidget(save_data_label)
        container_layout.addWidget(save_data_option)
        
        # container_layout.addLayout(save_data_config_layout)


        # maximize_window_config_layout = QHBoxLayout()
        maximize_window_label = QLabel("Maximize window on open")
        maximize_window_option = QComboBox()
        maximize_window_option.addItems(["True", "False"])
       
        container_layout.addWidget(maximize_window_label)
        container_layout.addWidget(maximize_window_option)
        
        # container_layout.addLayout(maximize_window_config_layout)


        # API URL CONFIGS
        mongo_config_label = QLabel("Enter your mongo uri label: ")
        self.mongo_url=QLineEdit()
        self.mongo_url.setPlaceholderText("enter mongo connnection string")

        container_layout.addWidget(mongo_config_label)
        container_layout.addWidget(self.mongo_url)

        ai_config_label = QLabel("Enter AI API url")
        self.ai_url_input = QLineEdit()
        self.ai_url_input.setPlaceholderText("https://api.com/")

        container_layout.addWidget(ai_config_label)
        container_layout.addWidget(self.ai_url_input)

        export_label = QLabel("Click to Export APP data in json: ")
        exportBtn = QPushButton("Export")

        container_layout.addWidget(export_label)
        container_layout.addWidget(exportBtn)

        self.containter.setLayout(container_layout)

        self.main_layout.addWidget(self.containter)
        self.main_layout.addStretch(0)
        self.setLayout(self.main_layout)
        self.setMinimumSize(400, 400)


app = QApplication([])
window = SettingsView()
window.show()
app.exec()