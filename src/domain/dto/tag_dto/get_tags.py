from dataclasses import dataclass
from typing import List, Dict


@dataclass
class GetTagsInputDto:
    pass


@dataclass
class GetTagsOutputDto:
    id: int
    name: str
