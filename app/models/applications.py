from typing import List
from sqlmodel import SQLModel, Field, Relationship


class ApplicationsBase(SQLModel):
    id: int = Field(primary_key=True)
    message: str | None
    status: str = Field(regex=r'PENDING|APPROVED|REJECTED')


class Application(ApplicationsBase, table=True):
    project_id: int = Field(foreign_key='project.id')
    project: 'Project' = Relationship(back_populates='applications')
    # candidate_id: 'Profile' = Relationship(back_populates='profile.user_id')
    candidate_id: List['Profile'] = Relationship(back_populates='profile.user_id')

