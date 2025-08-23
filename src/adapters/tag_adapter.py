from typing import List, Dict, Any
from dataclasses import asdict

from src.domain.dto.tag_dto.create_tag import CreateTagInputDto, CreateTagOutputDto
from src.domain.dto.tag_dto.update_tag import UpdateTagInputDto, UpdateTagOutputDto
from src.domain.dto.tag_dto.delete_tag import DeleteTagInputDto, DeleteTagOutputDto
from src.domain.dto.tag_dto.get_tags import GetTagsInputDto, GetTagsOutputDto


class TagAdapter:
    @classmethod
    def request_to_create_tag_input_dto(cls, create_tag_input_dto: dict) -> CreateTagInputDto:
        return CreateTagInputDto(**create_tag_input_dto)

    @classmethod
    def request_to_update_tag_input_dto(cls, update_tag_input_dto: dict) -> UpdateTagInputDto:
        return UpdateTagInputDto(**update_tag_input_dto)

    @classmethod
    def request_to_delete_tag_input_dto(cls, tag_id: int) -> DeleteTagInputDto:
        return DeleteTagInputDto(id=tag_id)

    @classmethod
    def request_to_get_tags_input_dto(cls) -> GetTagsInputDto:
        return GetTagsInputDto()

    @classmethod
    def create_tag_output_dto_to_response(cls, output_dto: CreateTagOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def update_tag_output_dto_to_response(cls, output_dto: UpdateTagOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def delete_tag_output_dto_to_response(cls, output_dto: DeleteTagOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def get_tags_output_dto_to_response(cls, output_dto: List[GetTagsOutputDto]) -> List[Dict[str, Any]]:
        return [asdict(item) for item in output_dto]
