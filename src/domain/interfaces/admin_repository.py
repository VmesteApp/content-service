from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.pulse import Pulse
from src.domain.dto.admin_dto.get_all_pulses import GetAllPulsesOutputDto


class AdminRepository(ABC):
    @abstractmethod
    def change_pulse_status(self, pulse_id: int, blocked: bool) -> bool:
        pass

    @abstractmethod
    def get_all_pulses(self, skip: int, limit: int) -> List[GetAllPulsesOutputDto]:
        pass

    @abstractmethod
    def create_pulse_admin(self, pulse: Pulse, tags: str) -> int:
        pass

    @abstractmethod
    def update_pulse_admin(self, pulse: Pulse, tags: str) -> bool:
        pass

    @abstractmethod
    def check_tag_exists(self, tag_id: int) -> bool:
        pass
