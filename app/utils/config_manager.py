"""
configManager.py

Purpose: 
    file configManager.py is used for setting a single instance of ConfigManager
Depends on:
    None

"""
from pathlib import Path
import logging
import traceback
from json import load, dump
logger = logging.getLogger(__name__)
class ConfigManager():
    _instance = None

    def __new__(cls): # overwritting the __new__ method which is called first when an object is initialized
        """
        Override __new__ method
        
        Args:
            cls: this represent the class itself
        """
        if cls._instance is None:
            # assign instance the class itselft
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # call __init__config
            cls._instance._init_config()


        return cls._instance

    def _init_config(self):
        """
        Method _init_config is use to set the path for file: settings.json
        Then sets self.settings with default values used for the application
        and calls the method load()
        """
        # Setup the app directory path
        self.app_dir = Path(__file__).resolve().parent.parent # /home/username/PROGRAMS/KALIDEV-TRACK/app/utils/configManager.py
        # set filename for settings.json
        self.settings_path =  self.app_dir /"setting.json" # or f"{self.app_dir}/settings.json" but this would change logic
        logger.debug("setting filepath: %s", self.settings_path)

        self.settings = {
            "theme": "dark",
            "font_family" : "Arial", 
            "email_for_notification": "",
            "save_before_exiting": "",
            "maximize_window_on_open": "",
            "mongodb_uri": "",
            "ai_url": ""
        }

        # call load() method
        self.load()

    
    def load(self):
        """
        Method load is used to read the settings of the application in settings.json and load them to self.settings dictionary
        """
        logger.debug("Method load executed")

        if self.settings_path.exists():
            try:
                # read file
                logger.debug("Reading settings.json file")
                
                with open(self.settings_path, 'r') as file:
                    data = load(file)
                    logger.debug("data from settings: %s", data)
                    self.settings.update(data)
                
            except Exception as err:
                # log error
                logger.debug("Error while reading settings.json file: %s", err)


    def save(self, data):
        """
        Method save is used to write data to settings.json file
        """
        logger.debug("Method save executed")
        full_error_details = traceback.format_exc()
        if self.settings_path.exists(): 
            try:
                with open(self.settings_path, 'w') as file:
                    dump(file, data)
            except Exception as err:
                logger.debug("Failed saving data: %s", full_error_details)


    def get(self, key): 
        if self.settings[key] is not None:
            return self.settings[key]


    def set(self, key, val) -> bool:
        if self.settings[key] is not None:
            self.settings[key] = val
            return True # operation success
        else:
            return False # operation not success