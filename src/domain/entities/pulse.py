from dataclasses import dataclass
from typing import Union


@dataclass
class Pulse:
    id: Union[int, None]
    category: str
    name: str
    founder_id: Union[int, None]
    description: str
    short_description: str
    images: Union[list, None]
    members: Union[list, None]
    tags: Union[list, None]
    blocked: Union[bool, None]
