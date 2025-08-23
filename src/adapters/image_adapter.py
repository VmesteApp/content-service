from typing import List, Dict, Any
from uuid import UUID
from dataclasses import asdict
from fastapi import UploadFile

from src.domain.dto.image_dto.upload_image import UploadImageInputDto, UploadImageOutputDto
from src.domain.dto.image_dto.get_image import GetImageInputDto, GetImageOutputDto
from src.domain.dto.image_dto.delete_image import DeleteImageInputDto, DeleteImageOutputDto


class ImageAdapter:
    @classmethod
    async def request_to_upload_image_input_dto(
        cls, 
        pulse_id: int, 
        user_id: int, 
        files: List[UploadFile]
    ) -> UploadImageInputDto:
        file_contents = []
        filenames = []
        
        for file in files:
            content = await file.read()
            file_contents.append(content)
            filenames.append(file.filename)
        
        return UploadImageInputDto(
            pulse_id=pulse_id,
            user_id=user_id,
            files=file_contents,
            filenames=filenames
        )

    @classmethod
    def request_to_get_image_input_dto(cls, image_uuid: UUID) -> GetImageInputDto:
        return GetImageInputDto(image_uuid=image_uuid)

    @classmethod
    def request_to_delete_image_input_dto(cls, image_uuid: UUID, user_id: int) -> DeleteImageInputDto:
        return DeleteImageInputDto(image_uuid=image_uuid, user_id=user_id)

    @classmethod
    def upload_image_output_dto_to_response(cls, output_dto: UploadImageOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def get_image_output_dto_to_response(cls, output_dto: GetImageOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)

    @classmethod
    def delete_image_output_dto_to_response(cls, output_dto: DeleteImageOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)
