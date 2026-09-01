import json
import os


class ReadTaskFiles():
    def __init__(self, filepath):
        self.data = []
        self.file = filepath
        self.project_tasks = []



    def readData(self):
        filename = "/home/alson-kali/PROGRAMMING/KALIDEV-TRACK/research/random_task_data.json"
        if (os.path.exists(filename) and os.path.isfile(filename)):
            with open(filename, 'r') as file:
                self.data = json.load(file)
                print("this is data from task file")
                print(self.data)


        # print(self.data["project"])
        # print(self.data["phases"])
        # print(len(self.data["phases"]))
        # print(data["subtasks"])


        if (len(self.data) > 0): # using len  on dictionary to check key properties if it's zero task file is empty
            return self.data 
            # count = 0
            # for item in self.data["phases"]:
            #     phase_name =  f"Phase {count + 1}: " + self.data["phases"][count]["name"] 
            #     phase_goal = self.data["phases"][count]["goal"] 

            #     # for subtasks
            #     subtasks_array = []
            #     subtaskcount = 0
            #     for subtasks in self.data["phases"][count]["subtasks"]:
            #         subtasks_dictionary = {"subtaskname": subtasks["subtaskname"], "subtaskdescription":  subtasks["description"],  "subtaskstatus": subtasks["status"] }
            #         subtasks_array.append(subtasks_dictionary)

            #     self.project_tasks.append([phase_name, phase_goal, subtasks_array])
            #     count += 1
        # return self.project_tasks

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
}
"""
