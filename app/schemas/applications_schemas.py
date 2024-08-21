from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Send_Application(BaseModel):
    project_id: int
    candidate_id: int
    message: str

class Verdict(BaseModel):
    id: int
    status: str