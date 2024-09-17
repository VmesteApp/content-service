from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Create_Pulse(BaseModel):
    category: str
    name: str
    description: str
    short_description: str
    tags: str

class Update_Pulse(BaseModel):
    id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str


class Delete_Pulse(BaseModel):
    id: int