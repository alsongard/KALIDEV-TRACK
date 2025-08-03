import json, os
class ReadWriteUpdateDeleteFileOperations():
    def __init__(self):

        self.data_array = []



    def readFiles(self):
        # check if PROJECTS folder exists
        home_dir = os.path.expanduser("~")
        app_project_folder = home_dir+"/"+"PROJECTS"

        # list everything in folder
        user_projects_folders = os.listdir(app_project_folder)


        # check if folder:
        for item in user_projects_folders:
            if not os.path.isfile(os.path.join(app_project_folder,item)): # item is not a file continue
                
                # set project path
                project_folder_path  = os.path.join(app_project_folder,item)
                print(f"project_folder_path: {project_folder_path}")
                
                # list files and directories
                get_all_files_dirs = os.listdir(os.path.join(app_project_folder,item))
                print(get_all_files_dirs)
                for item in get_all_files_dirs:
                    if os.path.isfile(os.path.join(project_folder_path, item)):
                        print(f"Found file: {item}")

                        # read the data in the file: json files
                        with open(os.path.join(project_folder_path, item), "r") as file:
                            data = json.load(file)
                            # print('Data is')
                            # print(data)
                            self.data_array.append(data)
        # print(self.data_array)
        return self.data_array
                
# read_instance = ReadWriteUpdateDeleteFileOperations()
# # print(read_instance.readFiles())
# geazy = read_instance.readFiles()
# print(f"This is geazy")
# print(geazy)