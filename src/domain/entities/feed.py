from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class FeedItem:
    id: int
    category: str
    name: str
    founder_id: int
    description: str
    short_description: str
    images: Optional[List[str]]
    tags: Optional[List[Dict[str, Any]]]
    created_at: Optional[str] = None
