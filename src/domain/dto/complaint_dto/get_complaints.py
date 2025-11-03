from dataclasses import dataclass
from typing import List


@dataclass
class GetComplaintsInputDto:
    pass


@dataclass
class GetComplaintsOutputDto:
    id: int
    pulse_id: int
    message: str
    status: str
