from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GetAllPulsesInputDto:
    skip: int = 0
    limit: int = 100


@dataclass
class GetAllPulsesOutputDto:
    id: int
    name: str
    created_at: str
    blocked: bool
