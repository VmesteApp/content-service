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