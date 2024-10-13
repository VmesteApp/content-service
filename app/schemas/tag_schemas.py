from pydantic import BaseModel


class CreateTag(BaseModel):
    name: str


class UpdateTag(BaseModel):
    id: int
    name: str


class DeleteTag(BaseModel):
    id: int
