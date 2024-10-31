from pydantic import BaseModel


class CreateСomplaint(BaseModel):
    message: str


class VerdictСomplaint(BaseModel):
    id: int
    verdict: str