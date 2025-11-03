from pydantic import BaseModel


class CreateComplaintSchema(BaseModel):
    message: str


class VerdictComplaintSchema(BaseModel):
    verdict: str


class ComplaintResponseSchema(BaseModel):
    id: int
    pulse_id: int
    message: str
    status: str

    class Config:
        from_attributes = True


class ComplaintsListResponseSchema(BaseModel):
    complaints: list[ComplaintResponseSchema]
