from typing import List
from abc import ABCMeta, abstractmethod

from src.domain.entities.application import Application


class ApplicationRepository(metaclass=ABCMeta):
    @abstractmethod
    def create_application(self, user_id: int, application: Application) -> bool:
        pass

    @abstractmethod
    def update_application(self, id: int, application: Application) -> bool:
        pass

    @abstractmethod
    def get_application_by_pulse_id(self, pulse_id: int) -> List[Application]:
        pass

    @abstractmethod
    def get_applications_by_user_id(self, user_id: int):
        pass
