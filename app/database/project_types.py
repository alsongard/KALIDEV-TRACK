from typing import Optional, Type, TypedDict, List
from pydantic import BaseModel, Field, ValidationError
class Subtask(BaseModel):
    module: str
    description: str
    Status: str


class Phase(BaseModel):
    phase_name: str
    phase_goal: str
    subtasks :List[Subtask]


class ProjectPhase(BaseModel):
    project_id: str
    project: str
    phases: List[Phase]


class ProjectInfo(BaseModel):
    project_title: str
    project_owner: str
    project_tags: List[str]
    project_description: str
    project_status: str
    project_priority: str
    project_start_date: str
    project_start_time: str
    project_end_date: str
    project_end_time: str
    initial_project_date_ending: str
    
    