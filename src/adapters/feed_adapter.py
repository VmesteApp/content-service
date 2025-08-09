from typing import List
from dataclasses import asdict

from src.domain.dto.pulse_dto.create_pulse import CreatePulseInputDto, CreatePulseOutputDto


class FeedAdapter:
    @classmethod
    def request_to_create_pulse_input_dto(cls, user_id: int, create_pulse_input_dto: dict) -> CreatePulseInputDto:
        create_pulse_input_dto['founder_id'] = user_id
        return CreatePulseInputDto(**create_pulse_input_dto)

    @classmethod
    def create_pulse_output_dto_to_response(cls, create_pulse_output_dto: CreatePulseOutputDto) -> str:
        return asdict(create_pulse_output_dto)
