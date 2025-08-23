from src.domain.dto.tag_dto.create_tag import CreateTagInputDto, CreateTagOutputDto
from src.domain.entities.tag import Tag
from src.domain.interfaces.tag_repository import TagRepository


class CreateTag:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository

    def execute(self, dto: CreateTagInputDto) -> CreateTagOutputDto:
        tag = Tag(id=None, name=dto.name)

        try:
            tag_id = self.repository.create_tag(tag)
            return CreateTagOutputDto(
                id=tag_id, 
                is_success=True, 
                error_message=""
            )
        except Exception as error:
            return CreateTagOutputDto(
                id=None, 
                is_success=False, 
                error_message=str(error)
            )
