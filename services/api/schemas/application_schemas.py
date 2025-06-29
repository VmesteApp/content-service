from pydantic import BaseModel


class SendApplication(BaseModel):
    pulse_id: int
    message: str


class Verdict(BaseModel):
    status: str
