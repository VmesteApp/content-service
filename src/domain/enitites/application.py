from uuid import UUID, uuid4
from dataclasses import dataclass, field

from domain.enitites.project import Project
from domain.enitites.skill import Skill


@dataclass
class Application:
    id: UUID = field(default_factory=uuid4)
    project_id: Project
    founder_id: UUID
    description: str
    skills: list[Skill] = field(default_factory=list)
