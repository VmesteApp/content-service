from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.feed import FeedItem
from src.domain.dto.feed_dto.get_feed import GetFeedInputDto


class FeedRepository(ABC):
    @abstractmethod
    def get_feed_items(self, dto: GetFeedInputDto) -> List[FeedItem]:
        pass
