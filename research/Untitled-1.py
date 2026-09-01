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