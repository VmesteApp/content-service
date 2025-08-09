from typing import List

from src.domain.dto.application_dto.get_user_applications import GetUserApplicationsInputDto, GetUserApplicationsOutputDto
from src.domain.entities.application import Application
from src.domain.interfaces.application_repository import ApplicationRepository


class GetUserApplications:
    def __init__(self, repository: ApplicationRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetUserApplicationsInputDto) -> List[GetUserApplicationsOutputDto]:
        try:
            applications: Application = self.repository.get_applications_by_user_id(user_id=dto.user_id)
        except Exception as error:
            return error
        else:
            output_dto = [GetUserApplicationsOutputDto(
                application_id=application.id,
                pulse=application.pulse,
                message=application.message,
                status=application.status,
                error_message=application.error_message,
            ) for application in applications]
            return output_dto
