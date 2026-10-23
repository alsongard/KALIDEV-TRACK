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

    Attributes:
        data_array[]: An empty array 

    Example:
        >>> 
    """

    logger = logging.getLogger(__name__)
    def __init__(self):
        self.data_array = []



    def readProjectDirectories(self):
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
        home_dir = os.path.expanduser("~")
        app_project_folder = home_dir+"/"+"PROJECTS"
    
        if os.path.exists(app_project_folder): # path exists /home/user/PROJECTS
            user_projects_folders = os.scandir(app_project_folder) # retrieves list of dirs
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
                            print(f"Project Dir: {project_folder_path} and Found file: {item}") # Found file: project_data.json
                            
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
            self.createProjectFolder()
            return self.data_array
            # list everything in folder:~/username/PROJECTS
    
    
    def createProjectFolder(self):
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

    def readTaskFiles(self, given_file_path):
        self.data = []
        self.file_for_tasks = given_file_path
        filename = "/home/alson-kali/PROGRAMMING/KALIDEV-TRACK/research/random_task_data.json"
        if (os.path.exists(filename) and os.path.isfile(filename)):
            with open(filename, 'r') as file:
                self.data = json.load(file)
                # print("this is data from task file")
                # print(self.data)
        
        
        if (len(self.data) > 0): # using len  on dictionary to check key properties if it's zero task file is empty
            return self.data 
        
        return []


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
                    
    def updateProjectTasks(self, projectName, data):
        project_name = projectName
        project_data = data
        home_dir = os.path.expanduser("~")
        project_directory_path = home_dir+"/"+"PROJECTS/"+project_name

        print("project_data")
        print(project_data)

        if (os.path.exists(project_directory_path)): # check if file exist
            with os.scandir(project_directory_path) as entries:# the os.scandir() method returns an iterator of os.dirEntry objects
                for dirEntry in entries:
                    if dirEntry.is_file and dirEntry.name == "project_data.json":
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