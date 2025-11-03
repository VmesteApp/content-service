from src.domain.dto.pulse_dto.get_pulse import GetPulseInputDto, GetPulseOutputDto
from src.domain.entities.pulse import Pulse
from src.domain.interfaces.pulse_repository import PulseRepository


class GetPulse:
    def __init__(self, repository: PulseRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetPulseInputDto) -> GetPulseOutputDto:
        try:
            pulse: Pulse = self.repository.get_pulse(pulse_id=dto.pulse_id)
        except Exception as error:
            return error
        else:
            output_dto = GetPulseOutputDto(
                id=pulse.id,
                category=pulse.category,
                name=pulse.name,
                founder_id=pulse.founder_id,
                description=pulse.description,
                short_description=pulse.short_description,
                members=pulse.members,
                tags=pulse.tags,
                blocked=None,
                images=pulse.images,
            )
            return output_dto
