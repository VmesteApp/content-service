from pydantic import BaseModel


class ChangeStatusSchema(BaseModel):
    blocked: bool


class CreatePulseAdminSchema(BaseModel):
    category: str
    name: str
    description: str
    short_description: str
    user_id: int
    tags: str


class UpdatePulseAdminSchema(BaseModel):
    id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str


class PulseAdminResponseSchema(BaseModel):
    id: int
    name: str
    created_at: str
    blocked: bool

    class Config:
        from_attributes = True
