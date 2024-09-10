from abc import ABC, abstractmethod
from typing import Any

from domain.enitites.skill import Skill


class SkillREpository(ABC):

    @abstractmethod
    async def get(self, **filters: Any) -> Skill | None:
        pass

    @abstractmethod
    async def change_category(self, skill: Skill) -> bool:
        pass
