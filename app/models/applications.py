from typing import List
from sqlmodel import SQLModel, Field, Relationship


class ApplicationsBase(SQLModel):
    id: int = Field(primary_key=True)
    message: str | None
    status: str = Field(regex=r'PENDING|APPROVED|REJECTED')
    candidate_id: int
    project_id: int


class Application(ApplicationsBase, table=True):
    pass
    #project_id: int = Field(foreign_key='project.id')
    #project: 'Project' = Relationship(back_populates='applications')
    #candidate_id: List['Profile'] = Relationship(back_populates='profile.user_id')

