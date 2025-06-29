from typing import List, Union
from dataclasses import dataclass


@dataclass
class GetPulseInputDto:
    pulse_id: Union[int, None]
    user_id: Union[int, None]


@dataclass
class GetPulseOutputDto:
    id: int
    category: str
    name: str
    founder_id: int
    description: str
    short_description: str
    members: Union[List[int], None]
    images: Union[List[str], None]
    tags: Union[List[dict], None]
    blocked: Union[bool, None]
