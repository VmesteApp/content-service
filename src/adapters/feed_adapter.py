from typing import List, Dict, Any
from dataclasses import asdict

from src.domain.dto.feed_dto.get_feed import GetFeedInputDto, GetFeedOutputDto


class FeedAdapter:
    @classmethod
    def request_to_get_feed_input_dto(
        cls, 
        user_id: int, 
        skip: int, 
        limit: int, 
        tags: List[int] = None, 
        name: str = None
    ) -> GetFeedInputDto:
        return GetFeedInputDto(
            user_id=user_id,
            skip=skip,
            limit=limit,
            tags=tags,
            name=name
        )

    @classmethod
    def get_feed_output_dto_to_response(
        cls, 
        output_dto: List[GetFeedOutputDto]
    ) -> List[Dict[str, Any]]:
        return [asdict(item) for item in output_dto]