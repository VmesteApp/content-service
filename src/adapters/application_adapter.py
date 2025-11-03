from typing import List
from dataclasses import asdict

from src.domain.dto.application_dto.create_application import CreateApplicationInputDto, CreateApplicationOutputDto
from src.domain.dto.application_dto.update_application import UpdateApplicationInputDto, UpdateApplicationOutputDto
from src.domain.dto.application_dto.get_pulse_applications import GetPulseApplicationsInputDto, GetPulseApplicationsOutputDto
from src.domain.dto.application_dto.get_user_applications import GetUserApplicationsInputDto, GetUserApplicationsOutputDto


class ApplicationAdapter:
    @classmethod
    def request_to_create_application_input_dto(cls, create_application_input_dto: dict) -> CreateApplicationInputDto:
        return CreateApplicationInputDto(**create_application_input_dto)

    @classmethod
    def request_to_update_application_input_dto(cls, application_id: int, update_application_input_dto: dict) -> UpdateApplicationInputDto:
        update_application_input_dto['application_id'] = application_id
        return UpdateApplicationInputDto(**update_application_input_dto)

    @classmethod
    def request_to_get_pulse_applications_input_dto(cls, pulse_id: int) -> GetPulseApplicationsInputDto:
        get_pulse_applications_input_dto = {'pulse_id': pulse_id}
        return GetPulseApplicationsInputDto(**get_pulse_applications_input_dto)

    @classmethod
    def request_to_get_user_applications_input_dto(cls, user_id: int) -> GetUserApplicationsInputDto:
        get_user_applications_input_dto = {'user_id': user_id}
        return GetUserApplicationsInputDto(**get_user_applications_input_dto)

    @classmethod
    def create_applications_output_dto_to_responce(cls, create_applications_output_dto: CreateApplicationOutputDto) -> str:
        return asdict(create_applications_output_dto)

    @classmethod
    def update_application_output_dto_to_responce(cls, update_applications_output_dto: UpdateApplicationOutputDto) -> str:
        return asdict(update_applications_output_dto)

    @classmethod
    def get_pulse_applications_dto_to_responce(cls, get_pulse_applications_output_dto: List[GetPulseApplicationsOutputDto]) -> str:
        return asdict(get_pulse_applications_output_dto)

    @classmethod
    def get_user_applications_output_dto_to_responce(cls, get_user_applications_output_dto: List[GetUserApplicationsOutputDto]) -> str:
        return asdict(get_user_applications_output_dto)
