from typing import List
from src.domain.dto.tag_dto.get_tags import GetTagsInputDto, GetTagsOutputDto
from src.domain.entities.tag import Tag
from src.domain.interfaces.tag_repository import TagRepository


class GetTags:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetTagsInputDto) -> List[GetTagsOutputDto]:
        try:
            tags: List[Tag] = self.repository.get_all_tags()
            
            return [
                GetTagsOutputDto(id=tag.id, name=tag.name)
                for tag in tags
            ]
        except Exception as error:
            raise Exception(f"Failed to get tags: {str(error)}")
