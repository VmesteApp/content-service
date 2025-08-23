from uuid import UUID
from src.domain.dto.image_dto.delete_image import DeleteImageInputDto, DeleteImageOutputDto
from src.domain.interfaces.image_repository import ImageRepository


class DeleteImage:
    def __init__(self, repository: ImageRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: DeleteImageInputDto) -> DeleteImageOutputDto:
        try:
            if not self.repository.check_image_exists(dto.image_uuid):
                return DeleteImageOutputDto(
                    is_success=False,
                    error_message="Image not found"
                )

            success = self.repository.delete_image(dto.image_uuid)
            
            if success:
                return DeleteImageOutputDto(
                    is_success=True,
                    error_message=""
                )
            else:
                return DeleteImageOutputDto(
                    is_success=False,
                    error_message="Failed to delete image"
                )

        except Exception as error:
            return DeleteImageOutputDto(
                is_success=False,
                error_message=str(error)
            )
