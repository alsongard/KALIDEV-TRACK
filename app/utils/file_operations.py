"""
file_operation.py

Purpose:
    Provides the class FileManager is used to provide methods that load, read, write, update and delete files, to be specific json files


Exports:
    FileManager

"""
import logging
import json, os
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
class FileManager():
    """
    The class FileManager is used to provide methods that load, read, write, update and delete files, to be specific json files

    Attributes:
        data_array[]: An empty array 

    Example:
        >>> fileManager = FileManager()
        >>> fileManager.read_project_directories() # read project_data.json file in APP_FOLDER
    """

    def __init__(self):
        self.data_array = []
        home = os.path.expanduser("~")
        self.app_folder = home + "/PROJECTS"

        logger.info("FileManager instance created")




    def read_project_directories(self):
        """
        Read all projects files for each directory in PROJECTS directory
        
        Args: 
            self:  declare to which instance it belongs to(seperation)

        Returns:
            list[dictionaries]: Each dictionary has keys:
                - userId: string
                - project_title: string
                - project_owner: string
                - project_tags: string
                - project_description: string
                - project_status: string
                - project_priority: string
                - project_start_date: string
                - project_start_time: string
                - project_end_date: string
                - project_end_time: string 
            
            list[] : empty array

        Example:
            >>> 
        
        """
        logger.info("readProjectDirs called - reading project data fles in ~/PROJECTS")

        home_dir = os.path.expanduser("~")
        app_project_folder = home_dir+"/"+"PROJECTS"
        logger.debug("Resolved project directory: %s", app_project_folder)
        if os.path.exists(app_project_folder): # path exists /home/user/PROJECTS
            
            with os.scandir(app_project_folder) as user_projects_folders: # retrieves list of dirs
            # print("user_projects_folders") # user_projects_folders
            # print(user_projects_folders) # <posix.ScandirIterator object at 0x7f81a6d94c30   
            
                for item in user_projects_folders:
                # print(f"this is item: {item}") # this is item: <DirEntry 'KALIDEV-track'>
                    if item.is_dir(): # item is not a file continue
                        
                        # set project path
                        project_folder_path  = os.path.join(app_project_folder,item)
                        # print(f"project_folder_path: {project_folder_path}") # project_folder_path: /home/alson-kali/PROJECTS/KALIDEV-track
                        
                        # list files and directories
                        get_all_files_dirs = os.listdir(os.path.join(app_project_folder,item))
                        # print(get_all_files_dirs)
                        for item in get_all_files_dirs:
                            if os.path.isfile(os.path.join(project_folder_path, item)):
                                # print(f"Project Dir: {project_folder_path} and Found file: {item}") # Found file: project_data.json
                                logger.debug("Project directory: %s and found file %s", project_folder_path, item)
                                if item == "project_data.json":
                                    # print('Success in founding project_data.json') # testing:working
    
                                    # read the data in the file: json files
                                    with open(os.path.join(project_folder_path, item), "r") as file:
                                        data = json.load(file)
                                        
                                        # print('Data is')
                                        # print(data)
                                        self.data_array.append(data)
            # print(self.data_array)
            user_projects_folders.close() # close to release memory
            return self.data_array
        else: 
            logger.warning("Project folder %s does not exist", app_project_folder)
            self.createProjectFolder()
            return self.data_array
            # list everything in folder:~/username/PROJECTS
    
    
    def create_app_folder(self) -> Boolean:
        """
        The method is used to create a PROJECT directory in home directory for the user

        Args:
            None

        Returns:
            0: integer which shows the success of the operation
        """
        home_director = os.path.expanduser("~")
        
        os.mkdir(home_director+"/" + "PROJECTS")     
        return 0        


    def create_project_folder(self, project_name) -> Boolean:
        """
        The method create_project_folder is used to create a project directory  in the APP_PROJECT directory
        
        Args:
            - project_name : the  name of the new project which is used to create the new project directory
        """
        logger.debug("Creating project folder: %s", project_name)
        if not os.path.exists(self.app_folder):
            self.create_app_folder()
        
        # create project directory
        folder_path=self.app_folder + "/"+project_name
        if os.path.exists(folder_path): # project already exist
            return

        os.mkdir(folder_path)
        if os.path.isdir(folder_path):
            logger.debug("Created project directory:  %s", folder_path)
            return True
        else:
            logger.debug("Failed in creating project directory: %s", folder_path)
            return False




    def write_project_details(self, project_name, data) -> Boolean:
        """
        The method write_project_details is used to save the data in PROJECTS/project_name directory to  project_data.json file

        Args:
            project_name (string): name of the project which correlates to the new directory created
            data (dict) : a dictionary containing the project details
        
        Returns:
            Boolean:
                True: show operation success
                False: show operation failed
        """
        project_path_folder = self.app_folder + "/" + project_name
        if not os.path.exists(project_path_folder):
            return False
        
        try:
            filepath = project_path_folder + "/project_data.json"
            with open(filepath, 'w') as file:
                json.dump(data, file)
                logger.debug("project data saved successfully to project_data.json file")
                return True
        except  Exception as error:
            logger.debug("Error while saving project data: %s ", error) 
            return False




    def create_project_task_file(self, project_name):
        """
        Method create_project_task_file is used to create a project_task.json file in project directory in APP_FOLDER

        Args:
            - project_name : name of the new project whose directory is in APP_FOLDER
        """
        logger.info("Method create_project_task_file executed")
        project_path_folder = self.app_folder + "/" + project_name

        if not os.path.exists(project_path_folder):
            return False
        new_tasks_dictionary = {
            "project": project_name,
            "phases" : []
        }

        try:
            file_path = project_path_folder + "/project_task.json" 
            with open(file_path, "w") as file:
                json.dump(new_tasks_dictionary, file)
                logger.debug("Success creating project_task file: %s", file_path)
        except Exception as error:
            logger.debug("Error creating project_task file: %s", file_path)
        


    def read_project_task_file(self, project_name):
        """
        Load a project's task file from disk into memory.

        Reads ``PROJECTS/<project_name>/project_tasks.json``, parses the JSON,
        and stores the phase list on ``self.tasks_data``. The return value
        mirrors the stored attribute, so the caller can use either without
        a second disk read.

        Args:
            project_name (str):
            Name of the project. Resolves to the directory
            ``PROJECTS/<project_name>/`` under the app data folder.

        Returns:
            dict: A dictionary with the following. 
            
            .. code-block:: python

                {
                    "project": str, # name of the project
                    "phases: [ # a list of dictionary , with the dictionary having the following 
                        {
                            "phase name": str, # name of the phase
                            "phase goal": str, # goal of the pahse
                            "subtasks": [       # list of subtask dicts
                                {
                                    "module name": str,   # e.g. "db.sql"
                                    "module description": str,   # what the subtask does
                                    "status": str,        # "pending" | "completed" | ...
                                    "status_note": str,   # optional free-text note
                                }
                            ]
                        }, 
                        { ....}
                    ]
                }

            Returns ``{}`` if the file exists but contains no phases.

        Raises:
            FileNotFoundError: If ``project_tasks.json`` does not exist.
            json.JSONDecodeError: If the file exists but is not valid JSON.
            PermissionError: If the file cannot be read.

        Side Effects:
            Sets ``self.tasks_data`` to the same dictionary that is returned.

        Example:
            >>> reader = ReadWriteUpdateDeleteFileOperations()
            >>> tasks = reader.read_project_task_file("NestJS_Docs")
            >>> tasks["phases"]
            {'phase name': 'some string', ...}, {'phase name': 'some string', ...}
        """
        
        logger.info("read_project_task_file method executed")
        task_data = {}
        project_dir = self.app_folder + "/" + project_name
        logger.debug("project_dir : %s", project_dir)
        if os.path.exists(project_dir): # project directory exists
            logger.debug("project dir exists: %s", project_dir)
            file_name = project_dir + "/project_task.json"
            if os.path.exists(file_name): # check if file name exist
                # read project_tasks file
                logger.debug("filename exists: %s", file_name)
                try:
                    with open(file_name, 'r') as file:
                        task_data = json.load(file)
                        return task_data
                except Exception as error:
                    logger.debug("Error reading project_task file: %s", error)
            else:
                logger.debug("file project_task.json does not exist in: %s", file_name)
                # create project_taskf_file
                self.create_project_task_file(project_name)
                return task_data


            
        
        
        # if (len(task_data) > 0): # using len  on dictionary to check key properties if it's zero task file is empty
        return task_data 

    def read_single_project_data(self, project_name):
        """
        The method is used to read a single project_data.json file 

        Args:
            self: Used to provide distiction for different instances of the class 
            project_name: the sub-directory in the PROJECTS directory 

        Returns:
            dictionary{}: With the following keys:
                - userId: string
                - project_title: string
                - project_owner: string
                - project_tags: string
                - project_description: string
                - project_status: string
                - project_priority: string
                - project_start_date: string
                - project_start_time: string
                - project_end_date: string
                - project_end_time: string
            
            
            empty dictionary{}
        
        Example:
            >>> 
        """
        home_dir = os.path.expanduser("~")
        # print(f"home_dir: {home_dir}")
        # print(f"project_name: {project_name}")

        project_directory_path = home_dir+"/"+"PROJECTS/"+project_name
        # print(f"project_directory_path: {project_directory_path}")

        if (os.path.exists(project_directory_path)):
            # check if file exist
            with  os.scandir(project_directory_path) as entries:# the os.scandir() method returns an iterator of os.dirEntry objects
                for dirEntry in entries:
                    if dirEntry.is_file:
                        file_name = dirEntry.name
                        # print(f"File_name: {file_name}")
                        file_path=project_directory_path+"/"+file_name
                        with open(file_path, "r") as file:
                            data = json.load(file)
                            print("this is data in read_single_project_data")
                            print(data)
                            return data
                    else:
                        return {}
                    
    def update_project_tasks(self, projectName, data):
        """
        The method update_project_tasks is used to update the project phases and subtasks (project_task.json)

        Args: 
            projectName(string) : name of the project
            data(dict): Dictionary object of the data being updated
        
        Returns:
            Boolean: 
                - True: Operation Success
                - False: Operation Failed
        """
        project_name = projectName
        project_data = data

        project_directory_path = self.app_folder  + "/"+project_name
        logger.debug("project_directory_path: %s", project_directory_path)
        logger.debug("updating project_data: %s", project_data)

        if os.path.exists(project_directory_path): # check if file exist
            with os.scandir(project_directory_path) as entries:# the os.scandir() method returns an iterator of os.dirEntry objects
                for dirEntry in entries:
                    if dirEntry.is_file and dirEntry.name == "project_task.json":
                        file_name = dirEntry.name
                        file_path=project_directory_path+"/"+file_name
                        with open(file_path, "w") as file:
                            json.dump(data, file)
                            break
                    
                
            
            return True # show status of above operation: success
        else:
            return False # show status of above operation: false



"""
this is data from task file
{
    'project': 'my-app', 
    'phases': [
        {
            'name': 'Database schema seup (SQL Tables)',
            'goal': 'All tables created and ready for TypeORM integration.', 
            'subtasks': [
                {   
                    'subtaskname': 'Module', 
                    'description': 'Master database initialization(schema creation, UUID extensions)', 
                    'status': 'pending'
                }
            ]
        }
    ]

"""