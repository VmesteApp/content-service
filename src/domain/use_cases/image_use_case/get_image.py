from uuid import UUID
from src.domain.dto.image_dto.get_image import GetImageInputDto, GetImageOutputDto
from src.domain.interfaces.image_repository import ImageRepository


class GetImage:
    def __init__(self, repository: ImageRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetImageInputDto) -> GetImageOutputDto:
        try:
            if not self.repository.check_image_exists(dto.image_uuid):
                return GetImageOutputDto(
                    file_path="",
                    is_success=False,
                    error_message="There is no image with this id"
                )

            file_path = self.repository.get_image_path(dto.image_uuid)
            if not file_path:
                return GetImageOutputDto(
                    file_path="",
                    is_success=False,
                    error_message="Image file not found"
                )

            return GetImageOutputDto(
                file_path=file_path,
                is_success=True,
                error_message=""
            )

        except Exception as error:
            return GetImageOutputDto(
                file_path="",
                is_success=False,
                error_message=str(error)
            )
