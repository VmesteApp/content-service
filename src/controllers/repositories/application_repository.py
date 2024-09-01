from abc import ABC, abstractmethod
from typing import Any

from domain.enitites.applications import Application
from domain.enitites.skill import Skill


class ApplicationRepository(ABC):

    @abstractmethod
    async def get(self, filters: Any) -> Application | None:
        pass

    @abstractmethod
    async def add_skill(self, skill: Skill) -> bool:
        pass
