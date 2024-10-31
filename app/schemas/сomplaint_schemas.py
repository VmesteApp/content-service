from pydantic import BaseModel


class CreateСomplaint(BaseModel):
    message: str


class VerdictСomplaint(BaseModel):
    verdict: str
