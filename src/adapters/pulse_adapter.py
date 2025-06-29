from typing import List
from dataclasses import asdict

from src.domain.dto.pulse_dto.create_pulse import CreatePulseInputDto, CreatePulseOutputDto
from src.domain.dto.pulse_dto.delete_pulse import DeletePulseInputDto, DeletePulseOutputDto
from src.domain.dto.pulse_dto.get_pulse import GetPulseInputDto, GetPulseOutputDto
from src.domain.dto.pulse_dto.update_pulse import UpdatePulseInputDto, UpdatePulseOutputDto


class PulseAdapter:
    @classmethod
    def request_to_create_pulse_input_dto(cls, user_id: int, create_pulse_input_dto: dict) -> CreatePulseInputDto:
        create_pulse_input_dto['founder_id'] = user_id
        return CreatePulseInputDto(**create_pulse_input_dto)
    
    @classmethod
    def request_to_update_pulse_input_dto(cls, update_pulse_input_dto: dict) -> UpdatePulseInputDto:
        return UpdatePulseInputDto(**update_pulse_input_dto)

    @classmethod
    def request_to_delete_pulse_input_dto(cls, pulse_id: int) -> DeletePulseInputDto:
        delete_pulse_input_dto = {'id': pulse_id}
        return DeletePulseInputDto(**delete_pulse_input_dto)

    @classmethod
    def request_to_get_pulses_input_dto(cls, user_id: int) -> GetPulseInputDto:
        get_pulses_input_dto = {'pulse_id': None, 'user_id': user_id}
        return GetPulseInputDto(**get_pulses_input_dto)

    @classmethod
    def request_to_get_pulse_input_dto(cls, pulse_id: int) -> GetPulseInputDto:
        get_pulses_input_dto = {'pulse_id': pulse_id, 'user_id': None}
        return GetPulseInputDto(**get_pulses_input_dto)

    @classmethod
    def create_pulse_output_dto_to_responce(cls, create_pulse_output_dto: CreatePulseOutputDto) -> str:
        return asdict(create_pulse_output_dto)

    @classmethod
    def update_pulse_output_dto_to_responce(cls, update_pulse_output_dto: UpdatePulseOutputDto) -> str:
        return asdict(update_pulse_output_dto)

    @classmethod
    def delete_pulse_output_dto_to_responce(cls, delete_pulse_output_dto: DeletePulseOutputDto) -> str:
        return asdict(delete_pulse_output_dto)

    @classmethod
    def get_pulses_output_dto_to_responce(cls, get_pulses_output_dto: List[GetPulseOutputDto]) -> str:
        result = []
        for pulse in get_pulses_output_dto:
            result.append(asdict(pulse))
            del result[-1]['members']
            del result[-1]['tags']
        return result

    @classmethod
    def get_pulse_output_dto_to_responce(cls, get_pulse_output_dto: GetPulseOutputDto) -> str:
        return asdict(get_pulse_output_dto)
