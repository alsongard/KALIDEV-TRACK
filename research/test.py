from  app.database.db_manager import DatabaseManager
from app.database.project_repository import ProjectRepository 
import asyncio
from typing import Optional
async def quick_start():
    db_instance = DatabaseManager("setup your database manager url")
    
    project_repo = ProjectRepository(db_manager=db_instance)
    project_data = {
        "project_title": "KALIDEV-TRACK",
        "project_owner": "alsongard",
        "project_tags": ["Pyside6, python3, pymongo"], 
        "project_description": "Project management system", 
        "project_status": "In progress", 
        "project_priority": "10", 
        "project_start_date": "2026-10-30", 
        "project_start_time": "12-00 AM", 
        "project_end_date": "2026-11-06", 
        "project_end_time": "12-00 AM", 
        "initial_project_date_ending": "2026-10-30"
    }
    

    try:
        result = await project_repo.insert_project(project_data=project_data)
        print(result)

        if result: 
            print(f"result.acknowledged is {result}")
        else: 
            print(f"Operation failed: {result}")

        await db_instance.close()
    except Exception as err:
        print(f"Error: {err}")
asyncio.run(quick_start())