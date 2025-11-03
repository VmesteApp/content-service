from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GetFeedInputDto:
    user_id: int
    skip: int = 0
    limit: int = 100
    tags: Optional[List[int]] = None
    name: Optional[str] = None


@dataclass
class GetFeedOutputDto:
    id: int
    category: str
    name: str
    founder_id: int
    description: str
    short_description: str
    images: List[str]
    tags: List[dict]
