from src.domain.dto.tag_dto.update_tag import UpdateTagInputDto, UpdateTagOutputDto
from src.domain.entities.tag import Tag
from src.domain.interfaces.tag_repository import TagRepository


class UpdateTag:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: UpdateTagInputDto) -> UpdateTagOutputDto:
        tag = Tag(id=dto.id, name=dto.name)
        
        try:
            success = self.repository.update_tag(tag)
            return UpdateTagOutputDto(
                is_success=success, 
                error_message=""
            )
        except Exception as error:
            return UpdateTagOutputDto(
                is_success=False,
                error_message=str(error)
            )
