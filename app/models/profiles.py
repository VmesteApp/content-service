from typing import List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime


class ProfileBase(SQLModel):
    first_name: str = Field(max_length=30, regex=r'[^0-9]')
    last_name: str = Field(max_length=30, regex=r'[^0-9]')
    middle_name: str | None = Field(max_length=30, regex=r'[^0-9]')
    date_birthday: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    sex: str | None = Field(regex=r'M|W')
    city: str | None
    university: str | None
    bio: str | None


class Profile(ProfileBase, table=True):
    #skills: List['Skill'] = Relationship(back_populates='skill.id')
    user_id: int = Field(primary_key=True)
