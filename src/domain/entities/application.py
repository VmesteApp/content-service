from dataclasses import dataclass
from typing import Union


@dataclass
class Application:
    id: Union[int, None]
    pulse_id: Union[int, None]
    candidate_id: Union[int, None]
    message: str
    status: Union[str, None]
