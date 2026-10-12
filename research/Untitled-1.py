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

"""
Task read from file
[
    [
        'Phase 0: Database schema seup (SQL Tables)', 
        'All tables created and ready for TypeORM integration.', 
        [{'subtaskname': 'Module', 'subtaskdescription': 'Master database initialization(schema creation, UUID extensions)', 'subtaskstatus': 'pending'}]]
    
]
"""


"""

    def headerData(self, section, orientation, role=Qt.DisplayRole): # this methods returns a string for the header
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headers[section])
            else:
                return str(section+1)
"""


"""
[
    [
        'Phase 0: Database schema seup (SQL Tables)', 
        'All tables created and ready for TypeORM integration.', 
        [{'subtaskname': 'db.sql', 'subtaskdescription': 'Master database initialization(schema creation, UUID extensions)', 'subtaskstatus': 'pending'}, {'subtaskname': 'home.sql', 'subtaskdescription': 'Single-row table for Hero/Mission statement, Hero Image URL.', 'subtaskstatus': '✅ Completed'}]
    ],
    [   
        'Phase 0: Database schema seup (SQL Tables)', 
        'All tables created and ready for TypeORM integration.', 
        [
            {
                'subtaskname': 'db.sql',
                'subtaskdescription': 'Master database initialization(schema creation, UUID extensions)', 
                'subtaskstatus': 'pending'
            },
            {
                'subtaskname': 'home.sql',
                'subtaskdescription': 'Single-row table for Hero/Mission statement, Hero Image URL.',
                'subtaskstatus': '✅ Completed'
            }
        ]
    ]
]
this is all_sub_task_for_table
[['db.sql', 'Master database initialization(schema creation, UUID extensions)', 'pending'], ['home.sql', 'Single-row table for Hero/Mission statement, Hero Image URL.', '✅ Completed']]
this is all_sub_task_for_table
[['db.sql', 'Master database initialization(schema creation, UUID extensions)', 'pending'], ['home.sql', 'Single-row table for Hero/Mission statement, Hero Image URL.', '✅ Completed']]

"""



"""

this is data from task file : python output WHICH IS CORRECT FOR READING FILE FROM TASKS.JSON FILE
{
    'project': 'my-app', 
    'phases': [
        {
            'name': 'Database schema seup (SQL Tables)', 
            'goal': 'All tables created and ready for TypeORM integration.', 
            'subtasks': [
                            {
                                'subtaskname': 'db.sql', 
                                'description': 'Master database initialization(schema creation, UUID extensions)', 
                                'status': 'pending'
                            },
                            {
                                'subtaskname': 'home.sql', 
                                'description': 'Single-row table for Hero/Mission statement, Hero Image URL.', 
                                'status': '✅ Completed'
                            }
                        ]
        }, 
        {
            'name': 'Phase 2: NestJS Backend API Resources (Modules, Controllers, Services)', 
            'goal': 'Generate resources, define entities/DTOs, integrate TypeORM repositories, and test endpoints.', 
            'subtasks': [
                {
                    'subtaskname': 'Home module', 
                    'description': 'Manages the homepage introduction text, motto, and hero image URL.', 
                    'status': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'
                }
            ]
        }
    ]
}
"""

"""
Task read from file
[
    [
        'Phase 1: Database schema seup (SQL Tables)', 
        'All tables created and ready for TypeORM integration.', 
        [
            {
                'subtaskname': 'db.sql', 
                'subtaskdescription': 'Master database initialization(schema creation, UUID extensions)', 
                'subtaskstatus': 'pending'
            },
            {
                'subtaskname': 'home.sql', 
                'subtaskdescription': 'Single-row table for Hero/Mission statement, Hero Image URL.', 
                'subtaskstatus': '✅ Completed'
            }
        ]
    ], 
    [
        'Phase 2: Phase 2: NestJS Backend API Resources (Modules, Controllers, Services)', 'Generate resources, define entities/DTOs, integrate TypeORM repositories, and test endpoints.', 
        [
            {
                'subtaskname': 'Home module', 
                'subtaskdescription': 'Manages the homepage introduction text, motto, and hero image URL.', 
                'subtaskstatus': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'
            }
        ]
    ]
]

"""


"""
this is a single phaseContent 
[
    'Phase 1: Database schema seup (SQL Tables)', 
    'All tables created and ready for TypeORM integration.', 
    [
        {
            'subtaskname': 'db.sql', 
            'subtaskdescription': 'Master database initialization(schema creation, UUID extensions)', 
            'subtaskstatus': 'pending'
        }, 
        {
            'subtaskname': 'home.sql', 
            'subtaskdescription': 'Single-row table for Hero/Mission statement, Hero Image URL.', 
            'subtaskstatus': '✅ Completed'
        }
    ]
]
this is all_sub_task_for_table
[
    [
        'db.sql', 
        'Master database initialization(schema creation, UUID extensions)', 
        'pending'
    ], 
    [
        'home.sql', 
        'Single-row table for Hero/Mission statement, Hero Image URL.', 
        '✅ Completed'
    ]
]
```
this is a single phaseContent 
['Phase 2: Phase 2: NestJS Backend API Resources (Modules, Controllers, Services)', 'Generate resources, define entities/DTOs, integrate TypeORM repositories, and test endpoints.', [{'subtaskname': 'Home module', 'subtaskdescription': 'Manages the homepage introduction text, motto, and hero image URL.', 'subtaskstatus': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'}]]
this is all_sub_task_for_table
[['Home module', 'Manages the homepage introduction text, motto, and hero image URL.', ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)']]

"""





# Discoverying which data structure to use to pass to TableModel
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
                    'subtaskname': 'db.sql', 
                    'description': 'Master database initialization(schema creation, UUID extensions)', 
                    'status': 'pending'
                }, 
                {
                    'subtaskname': 'home.sql', 
                    'description': 'Single-row table for Hero/Mission statement, Hero Image URL.', 
                    'status': '✅ Completed'
                }
            ]
        }, 
        {
            'name': 'NestJS Backend API Resources (Modules, Controllers, Services)', 
            'goal': 'Generate resources, define entities/DTOs, integrate TypeORM repositories, and test endpoints.', 
            'subtasks': [
                {
                    'subtaskname': 'Home module', 
                    'description': 'Manages the homepage introduction text, motto, and hero image URL.', 
                    'status': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'
                }
            ]
        }
    ]
}

"""

""""
Task read from file
[['Phase 1: Database schema seup (SQL Tables)', 'All tables created and ready for TypeORM integration.', [{'subtaskname': 'db.sql', 'subtaskdescription': 'Master database initialization(schema creation, UUID extensions)', 'subtaskstatus': 'pending'}, {'subtaskname': 'home.sql', 'subtaskdescription': 'Single-row table for Hero/Mission statement, Hero Image URL.', 'subtaskstatus': '✅ Completed'}]], ['Phase 2: NestJS Backend API Resources (Modules, Controllers, Services)', 'Generate resources, define entities/DTOs, integrate TypeORM repositories, and test endpoints.', [{'subtaskname': 'Home module', 'subtaskdescription': 'Manages the homepage introduction text, motto, and hero image URL.', 'subtaskstatus': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'}]]]
"""

myProject =[
        {
            "phaseName": "Database schema seup (SQL Tables)", 
            "phaseGoal": "All tables created and ready for TypeORM integration.",
            "subTasks" : [
                {
                    "subtaskname": "db.sql",
                    "subtaskdescription": "Master database initialization(schema creation, UUID extensions)", 
                    'subtaskstatus': 'pending'
                },
                {
                    'subtaskname': 'home.sql', 
                    'subtaskdescription': 'Single-row table for Hero/Mission statement, Hero Image URL.', 
                    'subtaskstatus': '✅ Completed'
                }
            ]    
        }, 
        {
            "phaseName":  'Phase 2: NestJS Backend API Resources (Modules, Controllers, Services)',
            "phaseGoal": 'Generate resources, define entities/DTOs, integrate TypeORM repositories, and test endpoints.',
            "subTasks": [
                {
                    'subtaskname': 'Home module', 
                    'subtaskdescription': 'Manages the homepage introduction text, motto, and hero image URL.', 
                    'subtaskstatus': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'
                }
            ]
        }
    ]
        
            
        

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
"""
looking at self._data this is an array of dictionaries """
[{'subtaskname': 'Home module', 'description': 'Manages the homepage introduction text, motto, and hero image URL.', 'status': ' ✅ Fully Completed (Entity, DTO, Repository injection, Service logic, Insomnia tested)'}]




# METHOD HANDLER USED IN TABLE_VIEW_MANAGEMENT WHEN RETURNED_TASKS USES ARRAY FOR SETTING QTableView
"""
# using array for setting data to  QLable and QTable View 
for phase_content in returnedTaskData:
    self.phaseContentGroupBox = QGroupBox() # GroupBox to enable styling
    self.phaseLayout = QVBoxLayout() # layout for the self.phaseContentGroupBox
    self.phaseTable = QTableView()
    self.phaseTable.wordWrapTrue = True
    self.phaseName = QLabel()
    self.phaseName.setObjectName("phaseNameLabel")
    self.phaseGoal = QLabel()
    self.phaseGoal.setObjectName("phaseGoalLabel")



    print("this is a single phaseContent ")
    print(phase_content)
    self.phaseName.setText(phase_content[0]) # name
    self.phaseGoal.setText(f"Goal: {phase_content[1]}") # goal

    self.phaseLayout.addWidget(self.phaseName)
    self.phaseLayout.addWidget(self.phaseGoal)

    self.each_data = []

    for item in phase_content[2]: # array of dictionaries
        thetask = [item['subtaskname'], item["subtaskdescription"], item["subtaskstatus"]]
        self.each_data.append(thetask)


    print('this is all_sub_task_for_table')
    print(self.each_data)

    header_data = ["Module", "Description", "Status"]
    self.model = TableModel(self.each_data, header_data)
    self.phaseTable.setModel(self.model)
    self.phaseTable.resizeColumnsToContents()
    self.phaseLayout.addWidget(self.phaseTable)


    self.phaseContentGroupBox.setLayout(self.phaseLayout)
    self.verticalLayout.addWidget(self.phaseContentGroupBox)
"""