from src.domain.dto.pulse_dto.create_pulse import CreatePulseInputDto, CreatePulseOutputDto
from src.domain.entities.pulse import Pulse
from src.domain.interfaces.application_repository import ApplicationRepository


class CreateApplication:
    def __init__(self, repository: ApplicationRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: CreatePulseInputDto) -> CreatePulseOutputDto:
        pulse = Pulse(
            id=None,
            category=dto.category,
            name=dto.name,
            founder_id=dto.founder_id,
            description=dto.description,
            short_description=dto.short_description,
            tags=dto.tags,
            images=None,
            members=None,
            blocked=False
        )
        try:
            pulse_data_out = self.repository.create_pulse(pulse)
        except Exception as error:
            return CreatePulseOutputDto(id=None, is_success=False, error_message=str(error))
        else:
            return CreatePulseOutputDto(id=pulse_data_out, is_success=True, error_message="")
