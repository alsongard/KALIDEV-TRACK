import json, os
class ReadWriteUpdateDeleteFileOperations():
    def readProjectDirectories(self):
            home_dir = os.path.expanduser("~")
            app_project_folder = home_dir+"/"+"PROJECTS"
    
            if os.path.exists(app_project_folder):
                # print("path exists") # testing:works 
                # user_projects_folders = os.listdir(app_project_folder)
                user_projects_folders = os.scandir(app_project_folder)
    
                # check if no files/folders exist: means no project at the moment
                # check_no_files_no_dirs = next(user_projects_folders, None)
                # print(f"check_no_files_no_dirs: {check_no_files_no_dirs}")
                # if check_no_files_no_dirs == None:
                #     # print("runnign no_files_no_dirs")
                #     return self.data_array
    
                # check if folder in Os.DirEntry object:
                for item in user_projects_folders:
                    if item.is_dir(): # item is not a file continue
                        
                        # set project path
                        project_folder_path  = os.path.join(app_project_folder,item)
                        # print(f"project_folder_path: {project_folder_path}")
                        
                        # list files and directories
                        get_all_files_dirs = os.listdir(os.path.join(app_project_folder,item))
                        # print(get_all_files_dirs)
                        for item in get_all_files_dirs:
                            if os.path.isfile(os.path.join(project_folder_path, item)):
                                # print(f"Found file: {item}")
                                
                                # adding functionality to read only project_data.json
                                # Found file: project_data.json
                                # Found file: project_task.json
                                if item == "project_data.json":
                                    # print('Success in founding project_data.json') # testing:working
                                    # read the data in the file: json files
                                    with open(os.path.join(project_folder_path, item), "r") as file:
                                        data = json.load(file)
                                        # print('Data is')
                                        # print(data)
                                        self.data_array.append(data)
                # print(self.data_array)
                return self.data_array
            else: 
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