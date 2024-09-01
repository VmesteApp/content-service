from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class SkillCategory:
    id: UUID = field(default_factory=uuid4)
    category: str
