from typing import List
from abc import ABCMeta, abstractmethod

from src.domain.entities.pulse import Pulse


class PulseRepository(metaclass=ABCMeta):
    @abstractmethod
    def create_pulse(self, pulse: Pulse) -> int:
        pass

    @abstractmethod
    def update_pulse(self, pulse: Pulse) -> bool:
        pass

    @abstractmethod
    def delete_pulse(self, id: int) -> bool:
        pass

    @abstractmethod
    def get_all_pulses(self, user_id: int) -> List[Pulse]:
        pass

    @abstractmethod
    def get_pulse(self, pulse_id: int) -> Pulse:
        pass
