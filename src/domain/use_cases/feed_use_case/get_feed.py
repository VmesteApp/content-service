from typing import List
from src.domain.dto.feed_dto.get_feed import GetFeedInputDto, GetFeedOutputDto
from src.domain.entities.feed import FeedItem
from src.domain.interfaces.feed_repository import FeedRepository


class GetFeed:
    def __init__(self, repository: FeedRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetFeedInputDto) -> List[GetFeedOutputDto]:
        try:
            feed_items: List[FeedItem] = self.repository.get_feed_items(dto)
            
            return [
                GetFeedOutputDto(
                    id=item.id,
                    category=item.category,
                    name=item.name,
                    founder_id=item.founder_id,
                    description=item.description,
                    short_description=item.short_description,
                    images=item.images,
                    tags=item.tags
                )
                for item in feed_items
            ]
            
        except Exception as error:
            raise Exception(f"Failed to get feed: {str(error)}")
