from dataclasses import dataclass


@dataclass
class UpdateComplaintInputDto:
    complaint_id: int
    verdict: str


@dataclass
class UpdateComplaintOutputDto:
    is_success: bool
    error_message: str
