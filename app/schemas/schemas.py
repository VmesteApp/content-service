from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Create_Project(BaseModel):
    name: str
    description: str
    skills: str


class UPDATE_PROJECT(BaseModel):
    id: int
    name: str
    description: str
    skills: str


class DELETE_PROJECT(BaseModel):
    id: int


class Send_Application(BaseModel):
    project_id: int
    candidate_id: int
    message: str


class Update_Profile(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    middle_name: str
    date_birthday: datetime
    sex: str
    city: str
    university: str
    bio: str


class Verdict(BaseModel):
    id: int
    status: str

