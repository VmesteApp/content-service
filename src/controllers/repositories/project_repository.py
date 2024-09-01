from abc import ABC, abstractmethod
from typing import Any

from domain.enitites.project import Project
from domain.enitites.skill import Skill
from domain.enitites.profile import Profile


class ProjectRepository(ABC):

    @abstractmethod
    async def get(self, **filters: Any) -> Project | None:
        pass

    @abstractmethod
    async def add_skill(self, skill: Skill) -> bool:
        pass

    @abstractmethod
    async def add_member(self, member: Profile) -> bool:
        pass
