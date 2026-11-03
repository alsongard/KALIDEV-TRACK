"""
settings_view.py

Purpose: 
    Provides the SettingsView class, which is a QWidget that represents the settings view in the application. 
    This view allows users to configure various settings related to the application.

Depends:
    - app.utils/.config_manager.ConfigManager
"""
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QWidget, QComboBox, QGroupBox, QVBoxLayout, QLabel
import logging

from  app.utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class SettingsView(QWidget):
    """
    A QWidget that represents the settings view in the application.
    """

    closed = Signal()
    def __init__(self):
        """
        Class constructor method
        """
        super().__init__()
     

        self.main_layout = QVBoxLayout() 
        self.containter = QGroupBox()
        container_layout= QVBoxLayout()
        self.configManager = ConfigManager()

        title_save_layout = QHBoxLayout()
        title_label = QLabel("Settings")
        title_label.setStyleSheet("font-weight:bold; font-size:18px")
        saveBtn = QPushButton("Save")
        saveBtn.clicked.connect(self.save_settings)
        title_save_layout.addWidget(title_label)
        title_save_layout.addWidget(saveBtn)

        description_label = QLabel("Configure settings for your application")

        self.main_layout.addLayout(title_save_layout)
        self.main_layout.addWidget(description_label)

        # dark_mode_layout = QHBoxLayout()
        self.dark_mode_settings= QComboBox()
        dark_label = QLabel("Dark Mode Settings")
        self.dark_mode_settings.addItems(["True", "False"])

        container_layout.addWidget(dark_label)
        container_layout.addWidget(self.dark_mode_settings)



        email_label = QLabel("Enter email used for notifications: ")
        self.email_for_notification = QLineEdit()
        self.email_for_notification.setPlaceholderText("Set email for notification")

        container_layout.addWidget(email_label)
        container_layout.addWidget(self.email_for_notification)

        # save_data_config_layout = QHBoxLayout()
        save_data_label=QLabel("Save data before exiting: ")
        self.save_data_option = QComboBox()
        self.save_data_option.addItems(["True", "False"])
        
        container_layout.addWidget(save_data_label)
        container_layout.addWidget(self.save_data_option)
        
        # container_layout.addLayout(save_data_config_layout)


        # maximize_window_config_layout = QHBoxLayout()
        maximize_window_label = QLabel("Maximize window on open")
        self.maximize_window_option = QComboBox()
        self.maximize_window_option.addItems(["True", "False"])
       
        container_layout.addWidget(maximize_window_label)
        container_layout.addWidget(self.maximize_window_option)
        
        # container_layout.addLayout(maximize_window_config_layout)


        # API URL CONFIGS
        mongo_config_label = QLabel("Enter your mongo uri label: ")
        self.mongo_url_input = QLineEdit()
        self.mongo_url_input.setPlaceholderText("enter mongo connnection string")

        container_layout.addWidget(mongo_config_label)
        container_layout.addWidget(self.mongo_url_input)

        ai_config_label = QLabel("Enter AI API url")
        self.ai_url_input = QLineEdit()
        self.ai_url_input.setPlaceholderText("https://api.com/")

        container_layout.addWidget(ai_config_label)
        container_layout.addWidget(self.ai_url_input)

        export_label = QLabel("Click to Export APP data in json: ")
        exportBtn = QPushButton("Export")

        container_layout.addWidget(export_label)
        container_layout.addWidget(exportBtn)

        self.set_settings() # sets the QWidgets to the current settings of application in settings.json

        self.containter.setLayout(container_layout)

        self.main_layout.addWidget(self.containter)
        self.main_layout.addStretch(0)
        self.setLayout(self.main_layout)
        self.setMinimumSize(400, 400)

    def closeEvent(self, event) -> None:
        self.closed.emit()
        return super().closeEvent(event)

    def save_settings(self):
        """
        Method save_settings is used to save configuration set by the user for the applicaton
        """

        dark_mode_setting = self.dark_mode_settings.currentText()
        email_setting = self.email_for_notification.text()
        save_data_setting = self.save_data_option.currentText()
        maximize_window_setting = self.maximize_window_option.currentText()
        mongo_uri_setting = self.mongo_url_input.text()
        ai_url_setting = self.ai_url_input.text()

        self.configManager.set("theme", dark_mode_setting)
        self.configManager.set("font_family", "")
        self.configManager.set("email_for_notification", email_setting)
        self.configManager.set("save_before_exiting", save_data_setting)
        self.configManager.set("maximize_window_on_open", maximize_window_setting)
        self.configManager.set("mongodb_uri", mongo_uri_setting)
        self.configManager.set("ai_url", ai_url_setting)

        result = self.configManager.save()
        if result:
            QMessageBox.information(
                self,
                "Informatiion",
                "Settings information has been updated",
                buttons=QMessageBox.StandardButton.Ok,
            )
        else:
            QMessageBox.warning(
                self,
                "Warning",
                "Error saving data",
                buttons=QMessageBox.StandardButton.Ok
            )


    def set_settings(self):
        """
        Method set_settings is used to set the current settings in settings.json file for SettingsView widget
        """
        logger.debug("set_settings method executed")

        if self.configManager.get("theme") == "True":
            self.dark_mode_settings.setCurrentIndex(0)
        else:
            self.dark_mode_settings.setCurrentIndex(1)


        self.email_for_notification.setText(self.configManager.get("email_for_notification"))


        if self.configManager.get("save_before_exiting") == "True":
            self.save_data_option.setCurrentIndex(0)
        else: 
            self.save_data_option.setCurrentIndex(1)


        if self.configManager.get("maximize_window_on_open") == "True":
            self.maximize_window_option.setCurrentIndex(0)
        else:
            self.maximize_window_option.setCurrentIndex(1)


        self.mongo_url_input.setText(self.configManager.get("mongodb_uri"))
        self.ai_url_input.setText(self.configManager.get("ai_url"))


# app = QApplication([])
# window = SettingsView()
# window.show()
# app.exec()