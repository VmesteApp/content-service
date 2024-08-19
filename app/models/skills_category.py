from typing import List
from sqlmodel import SQLModel, Field, Relationship


class SkillCategory(SQLModel, table=True):
    id: int = Field(primary_key=True)
    category: str
    skills: List['Skill'] = Relationship(back_populates='category')
