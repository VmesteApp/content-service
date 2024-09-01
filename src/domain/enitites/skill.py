from uuid import UUID, uuid4
from dataclasses import dataclass, field

from domain.enitites.skills_category import SkillCategory


@dataclass
class Skill:
    id: UUID = field(default_factory=uuid4)
    tag: str
    description: str
    category: SkillCategory
