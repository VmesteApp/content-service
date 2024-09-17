from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Create_Tag(BaseModel):
    name: str


class Update_Tag(BaseModel):
    id: int
    name: str


class Delete_Tag(BaseModel):
    id: int
