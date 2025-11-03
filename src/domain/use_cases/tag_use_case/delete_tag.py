from src.domain.dto.tag_dto.delete_tag import DeleteTagInputDto, DeleteTagOutputDto
from src.domain.interfaces.tag_repository import TagRepository


class DeleteTag:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: DeleteTagInputDto) -> DeleteTagOutputDto:
        try:
            success = self.repository.delete_tag(dto.id)
            return DeleteTagOutputDto(
                is_success=success, 
                error_message=""
            )
        except Exception as error:
            return DeleteTagOutputDto(
                is_success=False, 
                error_message=str(error)
            )
