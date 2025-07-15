import json
import os
project_details_dic = {
    "title": "Rets",
    "description": "this project is for this..",
    "start-date": "start-date",
    "end-date": "end-date",
    "priority": 'level'
}


def WriteReadProject():
    with open("./data/projectData.json", "a") as file:
        file.write(f"title: project 1\n")
        file.write("Project Decscription: This project is for this...\n")
        file.write("Project Start Date: start-date\n")
        file.write("Project End Date: end-date\n")
        file.write("Project Priority level: 10\n")


def WriteProject(filePath):
    with open(filePath, "w") as file:
        json.dump(project_details_dic,  file)

new_file_path="./data/projectData.json"
# WriteProject(new_file_path)
# WriteReadProject()

def ReadJSON(filepath):
    with open(filepath, 'r') as file:
        projectData = json.load(file)
        print(f'Project Data : {projectData}')

# ReadJSON(new_file_path)
def ReadProjectData(filepath):
    with open(filepath, "r") as file:
        projectArrayStrings = file.readlines()
        print(projectArrayStrings)# arrray : ['title: project 1\n', 'Project Decscription: This project is for this...\n',]
        for item in projectArrayStrings:
            if item.startswith("Project Start"):
                print(f'Got start date: {item}')
            print(f"Item : {item}")

myFile_path="./data/projectData.txt"
# ReadProjectData(myFile_path)


"""
import os
projectTitle = "New Project"
# check if projectTitle is given
if projectTitle:
    os.mkdir(f"data/{projectTitle}")
"""

# interesting solution can also work for passwords
def AmazingSolution(filepath, newProject):
    # check if filepath exist
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        # read file
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        # create an empty array
        data = []
    data.append(newProject)

    with open(filepath, 'w') as file:
        json.dump(data, file)



        

AmazingSolution(new_file_path, project_details_dic) 