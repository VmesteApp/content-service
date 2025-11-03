from src.domain.dto.pulse_dto.delete_pulse import DeletePulseInputDto, DeletePulseOutputDto
from src.domain.interfaces.pulse_repository import PulseRepository


class DeletePulse:
    def __init__(self, repository: PulseRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: DeletePulseInputDto) -> DeletePulseOutputDto:
        try:
            self.repository.delete_pulse(dto.id)
        except Exception as error:
            return DeletePulseOutputDto(is_success=False, error_message=str(error))
        else:
            return DeletePulseOutputDto(is_success=True, error_message="")
