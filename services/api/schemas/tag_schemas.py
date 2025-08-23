from pydantic import BaseModel


class CreateTagSchema(BaseModel):
    name: str


class UpdateTagSchema(BaseModel):
    id: int
    name: str


class TagResponseSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
