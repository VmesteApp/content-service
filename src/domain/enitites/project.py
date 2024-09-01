from uuid import UUID, uuid4
from dataclasses import dataclass, field

from domain.enitites.profile import Profile
from domain.enitites.skill import Skill


@dataclass
class Project:
    id: UUID = field(default_factory=uuid4)
    name: str
    description: str
    skills: list[Skill] = field(default_factory=list)
    members: list[Profile] = field(default_factory=list)
