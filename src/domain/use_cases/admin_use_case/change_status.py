from src.domain.dto.admin_dto.change_status import ChangeStatusInputDto, ChangeStatusOutputDto
from src.domain.interfaces.admin_repository import AdminRepository


class ChangeStatus:
    def __init__(self, repository: AdminRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: ChangeStatusInputDto) -> ChangeStatusOutputDto:
        try:
            success = self.repository.change_pulse_status(dto.pulse_id, dto.blocked)
            return ChangeStatusOutputDto(
                is_success=success,
                error_message=""
            )
        except Exception as error:
            return ChangeStatusOutputDto(
                is_success=False,
                error_message=str(error)
            )
