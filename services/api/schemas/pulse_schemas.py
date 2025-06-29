from pydantic import BaseModel


class CreatePulseSchemas(BaseModel):
    category: str
    name: str
    description: str
    short_description: str
    tags: str


class UpdatePulseSchemas(BaseModel):
    id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str
