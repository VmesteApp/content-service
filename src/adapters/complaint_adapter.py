from typing import List, Dict, Any
from dataclasses import asdict

from src.domain.dto.complaint_dto.create_complaint import CreateComplaintInputDto, CreateComplaintOutputDto
from src.domain.dto.complaint_dto.get_complaints import GetComplaintsInputDto, GetComplaintsOutputDto
from src.domain.dto.complaint_dto.update_complaint import UpdateComplaintInputDto, UpdateComplaintOutputDto


class ComplaintAdapter:
    @classmethod
    def request_to_create_complaint_input_dto(cls, pulse_id: int, data: dict) -> CreateComplaintInputDto:
        return CreateComplaintInputDto(pulse_id=pulse_id, message=data["message"])

    @classmethod
    def request_to_get_complaints_input_dto(cls) -> GetComplaintsInputDto:
        return GetComplaintsInputDto()

    @classmethod
    def request_to_update_complaint_input_dto(cls, complaint_id: int, data: dict) -> UpdateComplaintInputDto:
        return UpdateComplaintInputDto(complaint_id=complaint_id, verdict=data["verdict"])

    @classmethod
    def create_complaint_output_dto_to_response(cls, output_dto: CreateComplaintOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def get_complaints_output_dto_to_response(cls, output_dto: List[GetComplaintsOutputDto]) -> Dict[str, Any]:
        return {"complaints": [asdict(item) for item in output_dto]}

    @classmethod
    def update_complaint_output_dto_to_response(cls, output_dto: UpdateComplaintOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)
