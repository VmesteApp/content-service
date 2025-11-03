from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.tag import Tag


class TagRepository(ABC):
    @abstractmethod
    def create_tag(self, tag: Tag) -> int:
        pass

    @abstractmethod
    def update_tag(self, tag: Tag) -> bool:
        pass

    @abstractmethod
    def delete_tag(self, tag_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_tags(self) -> List[Tag]:
        pass
