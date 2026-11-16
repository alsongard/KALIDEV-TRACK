"""
project_repository.py

Purpose:
    Provides class ProjectRepository used for project backup and synchronization.

"""


import logging

logger = logging.getLogger(__name__)
from app.database.project_types import ProjectInfo
from app.database.db_manager import DatabaseManager
class ProjectRepository():
    """
    Class ProjectRepository provides methods for backing up the projects data.
    """
    def __init__(self, db_manager: DatabaseManager):
        devdb = db_manager.db
        self.project_collection = devdb["projects_info"]
        self.phase_collection = devdb["project_phase"]

    

    async def insert_project(self, project_data:dict) -> bool:
        """
        Method insert_project is used for inserting a single project data
        
        Args:
            project_data(dict) : Project fields to insert
                Keys: project_title,  project_owner,  project_tags,  project_description,  project_status,  project_priority,  project_start_date,  project_start_time,  project_end_date,  project_end_time,  

        Returns: 
            bool:
                True : insert succeeded
                False: insert failed
        """
        validated_project = ProjectInfo(**project_data)
        logger.info("Running insert_project")
        result = await self.project_collection.insert_one(validated_project.model_dump())
        if result.acknowledged: 
            return True
        else:
            return False


    async def update_project(self, project_id, update_project):
        """
        Method update_project is used to upate the project data
        """
        logger.info("Running update_project")


    async def delete_project(self, project_id):
        """
        Method delete_project is used to delete the project in the database
        """
        logger.info("Running delete_project")


    async def get_project(self, project_name):
        """
        Method get_project is used to get the project  based on a project name
        """
        logger.info("Running get_project")


    async def get_all_projects(self, ):
        """
        Method get_all_projects is used to get all projects from the online database 
        """
        logger.info("Running get_all_projects")



    async def insert_project_phase(self, phase_data):
        """
        Method insert_project_phase is used to backup a project  phase and subtasks
        """
        logger.info("Running insert_project_phase")
        result = await self.phase_collection.insert_one(phase_data)
        if result.acknowledged:
            return True
        else:
            return False

    async def update_project_phase(self, project_id, updated_phase):
        """
        Method update_project_phase is used to update the project phase data
        """
        logger.info("Running update_project_phase")


    async def delete_project_phases(self, project_id):
        """
        Method delete_project_phase is used to delete a project phase based on the project_id
        """
        logger.info("Running delete_project_phases")


    async def get_project_phase(self, project_id):
        """
        Method get_project_phase is used to get a projects phase data based on the project_id
        """
        logger.info("Running get_project_phase")
        