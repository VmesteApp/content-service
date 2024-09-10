from abc import ABC, abstractmethod
from typing import Any

from domain.enitites.profile import Profile
from domain.enitites.skill import Skill


class ProfileRepository(ABC):

    @abstractmethod
    async def get(self, **filters: Any) -> Profile | None:
        pass
    
    @abstractmethod
    async def add_skill(self, skill: Skill) -> bool:
        pass
