from src.domain.dto.application_dto.update_application import UpdateApplicationInputDto, UpdateApplicationOutputDto
from src.domain.entities.application import Application
from src.domain.interfaces.application_repository import ApplicationRepository


class UpdateApplication:
    def __init__(self, repository: ApplicationRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: UpdateApplicationInputDto) -> UpdateApplicationOutputDto:
        application = Application(
            id=dto.id,
            pulse_id=None,
            candidate_id=None,
            message='',
            status=dto.status,
        )
        try:
            self.repository.update_application(application)
        except Exception as error:
            return UpdateApplicationOutputDto(is_success=False, error_message=str(error))
        else:
            return UpdateApplicationOutputDto(is_success=True, error_message="")
