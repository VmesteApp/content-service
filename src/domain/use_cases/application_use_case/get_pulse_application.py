from typing import List

from src.domain.dto.application_dto.get_pulse_applications import GetPulseApplicationsInputDto, GetPulseApplicationsOutputDto
from src.domain.entities.application import Application
from src.domain.interfaces.application_repository import ApplicationRepository


class GetPulseApplications:
    def __init__(self, repository: ApplicationRepository) -> None:
        self.repository = repository

    def execute(self, dto: GetPulseApplicationsInputDto) -> List[GetPulseApplicationsOutputDto]:
        try:
            applications: List[Application] = self.repository.get_application_by_pulse_id(pulse_id=dto.pulse_id)
        except Exception as error:
            return error
        else:
            output_dto = [GetPulseApplicationsOutputDto(
                application_id=application.application_id,
                pulse_id=application.pulse_id,
                candidate_id=application.candidate_id,
                message=application.message,
                status=application.status,
            ) for application in applications]
            return output_dto
