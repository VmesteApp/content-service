from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from src.domain.entities.image import Image


class ImageRepository(ABC):
    @abstractmethod
    def create_image(self, image: Image) -> bool:
        pass

    @abstractmethod
    def get_image_path(self, image_uuid: UUID) -> Optional[str]:
        pass

    @abstractmethod
    def delete_image(self, image_uuid: UUID) -> bool:
        pass

    @abstractmethod
    def get_images_count(self, pulse_id: int) -> int:
        pass

    @abstractmethod
    def check_pulse_exists(self, pulse_id: int) -> bool:
        pass

    @abstractmethod
    def check_image_exists(self, image_uuid: UUID) -> bool:
        pass

    @abstractmethod
    def check_user_has_access(self, pulse_id: int, user_id: int) -> bool:
        pass
