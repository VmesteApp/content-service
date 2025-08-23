from src.domain.dto.admin_dto.create_pulse_admin import CreatePulseAdminInputDto, CreatePulseAdminOutputDto
from src.domain.entities.pulse import Pulse
from src.domain.interfaces.admin_repository import AdminRepository


class CreatePulseAdmin:
    ALLOWED_CATEGORIES = ["project", "event"]
    
    def __init__(self, repository: AdminRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: CreatePulseAdminInputDto) -> CreatePulseAdminOutputDto:
        try:
            if dto.category not in self.ALLOWED_CATEGORIES:
                return CreatePulseAdminOutputDto(
                    pulse_id=0,
                    is_success=False,
                    error_message="Invalid category"
                )
            
            if dto.tags:
                tag_ids = [int(tag.strip()) for tag in dto.tags.split(",") if tag.strip().isdigit()]
                for tag_id in tag_ids:
                    if not self.repository.check_tag_exists(tag_id):
                        return CreatePulseAdminOutputDto(
                            pulse_id=0,
                            is_success=False,
                            error_message=f"Tag with id {tag_id} does not exist"
                        )
            
            pulse = Pulse(
                id=None,
                category=dto.category,
                name=dto.name,
                founder_id=dto.user_id,
                description=dto.description,
                short_description=dto.short_description,
                images=None,
                members=None,
                tags=None,
                blocked=False
            )
            
            pulse_id = self.repository.create_pulse_admin(pulse, dto.tags)
            
            return CreatePulseAdminOutputDto(
                pulse_id=pulse_id,
                is_success=True,
                error_message=""
            )
            
        except Exception as error:
            return CreatePulseAdminOutputDto(
                pulse_id=0,
                is_success=False,
                error_message=str(error)
            )
