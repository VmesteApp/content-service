import os
from uuid import uuid4
from typing import List
from src.domain.dto.image_dto.upload_image import UploadImageInputDto, UploadImageOutputDto
from src.domain.entities.image import Image
from src.domain.interfaces.image_repository import ImageRepository


class UploadImage:
    def __init__(self, repository: ImageRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: UploadImageInputDto) -> UploadImageOutputDto:
        try:
            if not self.repository.check_pulse_exists(dto.pulse_id):
                return UploadImageOutputDto(
                    is_success=False,
                    error_message="There is no pulse with this id"
                )

            if not self.repository.check_user_has_access(dto.pulse_id, dto.user_id):
                return UploadImageOutputDto(
                    is_success=False,
                    error_message="Access denied"
                )

            current_count = self.repository.get_images_count(dto.pulse_id)
            if current_count + len(dto.files) > 100:
                return UploadImageOutputDto(
                    is_success=False,
                    error_message="You can't upload more than 100 images"
                )

            for file_content, filename in zip(dto.files, dto.filenames):
                unique_id = uuid4()
                file_extension = os.path.splitext(filename)[1]
                unique_filename = f"{unique_id}{file_extension}"

                image = Image(
                    image_id=unique_id,
                    pulse_id=dto.pulse_id,
                    full_name=unique_filename,
                    image_path=f"https://vmesteapp.ru/content/image/{unique_id}"
                )

                self.repository.create_image(image)

            return UploadImageOutputDto(
                is_success=True,
                error_message=""
            )

        except Exception as error:
            return UploadImageOutputDto(
                is_success=False,
                error_message=str(error)
            )
