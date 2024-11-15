from pydantic import BaseModel


class CreatePulse(BaseModel):
    category: str
    name: str
    description: str
    short_description: str
    tags: str


class UpdatePulse(BaseModel):
    id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str


class DeletePulse(BaseModel):
    id: int


class ChangeStatus(BaseModel):
    blocked: bool


class CreatePulseAdmin(BaseModel):
    user_id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str
