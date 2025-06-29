from src.domain.dto.pulse_dto.update_pulse import UpdatePulseInputDto, UpdatePulseOutputDto
from src.domain.entities.pulse import Pulse
from src.domain.interfaces.pulse_repository import PulseRepository


class UpdatePulse:
    def __init__(self, repository: PulseRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: UpdatePulseInputDto) -> UpdatePulseOutputDto:
        pulse = Pulse(
            id=dto.id,
            category=dto.category,
            name=dto.name,
            founder_id=None,
            description=dto.description,
            short_description=dto.short_description,
            tags=dto.tags,
            images=None,
            members=None,
            blocked=False
        )
        try:
            self.repository.update_pulse(pulse)
        except Exception as error:
            return UpdatePulseOutputDto(id=None, is_success=False, error_message=str(error))
        else:
            return UpdatePulseOutputDto(is_success=True, error_message="")
