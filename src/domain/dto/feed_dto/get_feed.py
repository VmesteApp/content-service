from typing import List
from dataclasses import dataclass

from src.domain.entities.pulse import Pulse


@dataclass
class GetFeedInputDto:
    user_id: int
    skip: int
    limit: int


# @dataclass
# class GetFeedOutputDto:
#     pulses: List[Pulse]
#     is_success: bool
#     error_message: str
