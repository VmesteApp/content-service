from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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