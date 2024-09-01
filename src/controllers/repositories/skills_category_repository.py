from abc import ABC, abstractmethod
from typing import Any

from domain.enitites.skills_category import SkillCategory


class SkillCategoryRepository(ABC):

    @abstractmethod
    async def get(self, **filters: Any) -> SkillCategory | None:
        pass
