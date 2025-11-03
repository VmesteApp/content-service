from src.domain.dto.application_dto.create_application import CreateApplicationInputDto, CreateApplicationOutputDto
from src.domain.entities.application import Application
from src.domain.interfaces.application_repository import ApplicationRepository


class CreateApplication:
    def __init__(self, repository: ApplicationRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: CreateApplicationInputDto) -> CreateApplicationOutputDto:
        application = Application(
            id=None,
            pulse_id=dto.pulse_id,
            candidate_id=dto.candidate_id,
            message=dto.message,
            status=None,
        )
        try:
            application_data_out = self.repository.create_application(application)
        except Exception as error:
            return CreateApplicationOutputDto(id=None, is_success=False, error_message=str(error))
        else:
            return CreateApplicationOutputDto(id=application_data_out, is_success=True, error_message="")
