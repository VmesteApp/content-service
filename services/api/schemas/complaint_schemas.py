from pydantic import BaseModel


class CreateComplaint(BaseModel):
    message: str


class VerdictComplaint(BaseModel):
    verdict: str
