import json, os
class ReadWriteUpdateDeleteFileOperations():
    def __init__(self):
        self.data_array = []


    def readProjectDirectories(self):
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
                            # print(f"Found file: {item}") # Found file: project_data.json
                            
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
                            return data
                    else:
                        return {}
                    
        
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