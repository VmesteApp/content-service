from typing import List

from src.domain.dto.pulse_dto.get_pulse import GetPulseInputDto, GetPulseOutputDto
from src.domain.entities.pulse import Pulse
from src.domain.interfaces.pulse_repository import PulseRepository


class GetPulses:
    def __init__(self, repository: PulseRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetPulseInputDto) -> List[GetPulseOutputDto]:
        try:
            pulses: List[Pulse] = self.repository.get_all_pulses(user_id=dto.user_id)
        except Exception as error:
            return error
        else:
            output_dto = [GetPulseOutputDto(
                id=pulse.id,
                category=pulse.category,
                name=pulse.name,
                founder_id=pulse.founder_id,
                description=pulse.description,
                short_description=pulse.short_description,
                blocked=pulse.blocked,
                images=pulse.images,
                members=None,
                tags=None,
            ) for pulse in pulses]

            return output_dto
