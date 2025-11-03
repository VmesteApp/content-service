from typing import List, Dict, Any
from dataclasses import asdict

from src.domain.dto.admin_dto.change_status import ChangeStatusInputDto, ChangeStatusOutputDto
from src.domain.dto.admin_dto.get_all_pulses import GetAllPulsesInputDto, GetAllPulsesOutputDto
from src.domain.dto.admin_dto.create_pulse_admin import CreatePulseAdminInputDto, CreatePulseAdminOutputDto
from src.domain.dto.admin_dto.update_pulse_admin import UpdatePulseAdminInputDto, UpdatePulseAdminOutputDto


class AdminAdapter:
    @classmethod
    def request_to_change_status_input_dto(cls, pulse_id: int, blocked: bool) -> ChangeStatusInputDto:
        return ChangeStatusInputDto(pulse_id=pulse_id, blocked=blocked)

    @classmethod
    def request_to_get_all_pulses_input_dto(cls, skip: int, limit: int) -> GetAllPulsesInputDto:
        return GetAllPulsesInputDto(skip=skip, limit=limit)

    @classmethod
    def request_to_create_pulse_admin_input_dto(cls, data: dict) -> CreatePulseAdminInputDto:
        return CreatePulseAdminInputDto(**data)

    @classmethod
    def request_to_update_pulse_admin_input_dto(cls, data: dict) -> UpdatePulseAdminInputDto:
        return UpdatePulseAdminInputDto(**data)

    @classmethod
    def change_status_output_dto_to_response(cls, output_dto: ChangeStatusOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def get_all_pulses_output_dto_to_response(cls, output_dto: List[GetAllPulsesOutputDto]) -> Dict[str, Any]:
        return {"pulses": [asdict(item) for item in output_dto]}

    @classmethod
    def create_pulse_admin_output_dto_to_response(cls, output_dto: CreatePulseAdminOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def update_pulse_admin_output_dto_to_response(cls, output_dto: UpdatePulseAdminOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)
