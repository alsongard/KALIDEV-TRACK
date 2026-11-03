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
        self.app_dir = Path(__file__).resolve().parent.parent.parent # /home/username/PROGRAMS/KALIDEV-TRACK/app/utils/configManager.py
        # set filename for settings.json
        logger.debug("app directory : %s", self.app_dir)
        self.settings_path =  self.app_dir /"setting.json" # or f"{self.app_dir}/settings.json" but this would change logic
        logger.debug("setting filepath: %s", self.settings_path)

        self.settings = {
            "theme": "True",
            "font_family" : "Arial", 
            "email_for_notification": "False",
            "save_before_exiting": "True",
            "maximize_window_on_open": "False",
            "mongodb_uri": "",
            "ai_url": ""
        }

        # call load() method
        self.load()

    
    def load(self):
        """
        # Method load is used to read the settings of the application in settings.json and load them to self.settings dictionary
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
        
        else: 
            logger.debug("file settings.json does not exist. path: %s", self.settings_path)
            self.create_settings_file()
            

    def create_settings_file(self):
        """
        Method create_settings_file is used to create a settings.json file if it does not exist
        """
        if self.app_dir.exists():
            # create file name settings.json
            if self.settings_path.exists() is False:

                with open(self.settings_path, 'w') as file:
                    dump(self.settings, file)


    def save(self) -> bool:
        """
        Method save is used to write data to settings.json file
        """
        logger.debug("Method save executed")
        if self.settings_path.exists(): 
            try:
                with open(self.settings_path, 'w') as file:
                    dump(self.settings, file)
                logger.debug("Data saved successfully")
                return True
            except Exception as err:
                full_error_details = traceback.format_exc()
                logger.debug("Failed saving data: %s", full_error_details)
                return False

        logger.debug("Error: %s does not exist", self.settings_path)
        return False # file does not exist


    def get(self, key): 
        """
        Method get is used to return a value from the self.settings dictionary

        - Args:
            key (string) : a key in self.settings dictionary
        """
        if self.settings[key] is not None:
            return self.settings[key]


    def set(self, key, val) -> bool:
        """
        Method set is used ot set a value for a key in self.settings dictionary

        - Args:
            key (string) : a key in self.settings dictionary
            val (string) : a value in self.settings dictionary

        Return:
            True: Operation Success
            False: Operation False
        """
        if self.settings[key] is not None:
            self.settings[key] = val
            return True # operation success
        else:
            return False # operation not success