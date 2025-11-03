from src.domain.dto.admin_dto.update_pulse_admin import UpdatePulseAdminInputDto, UpdatePulseAdminOutputDto
from src.domain.entities.pulse import Pulse
from src.domain.interfaces.admin_repository import AdminRepository


class UpdatePulseAdmin:
    ALLOWED_CATEGORIES = ["project", "event"]
    
    def __init__(self, repository: AdminRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: UpdatePulseAdminInputDto) -> UpdatePulseAdminOutputDto:
        try:
            if dto.category not in self.ALLOWED_CATEGORIES:
                return UpdatePulseAdminOutputDto(
                    is_success=False,
                    error_message="Invalid category"
                )
            
            if dto.tags:
                tag_ids = [int(tag.strip()) for tag in dto.tags.split(",") if tag.strip().isdigit()]
                for tag_id in tag_ids:
                    if not self.repository.check_tag_exists(tag_id):
                        return UpdatePulseAdminOutputDto(
                            is_success=False,
                            error_message=f"Tag with id {tag_id} does not exist"
                        )
            
            pulse = Pulse(
                id=dto.id,
                category=dto.category,
                name=dto.name,
                founder_id=None,
                description=dto.description,
                short_description=dto.short_description,
                images=None,
                members=None,
                tags=None,
                blocked=None
            )
            
            success = self.repository.update_pulse_admin(pulse, dto.tags)
            
            return UpdatePulseAdminOutputDto(
                is_success=success,
                error_message=""
            )
            
        except Exception as error:
            return UpdatePulseAdminOutputDto(
                is_success=False,
                error_message=str(error)
            )
