from typing import List
from sqlmodel import SQLModel, Field, Relationship


class ProjectBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=50)
    description: str


class Project(ProjectBase, table=True):
    skills: str
    applications: List['Application'] = Relationship(back_populates='application.project_id')
