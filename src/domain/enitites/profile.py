from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import date

from domain.enitites.skill import Skill


@dataclass
class Profile:
    id: UUID = field(default_factory=uuid4)
    first_name: str
    last_name: str
    middle_name: str
    sex: str
    city: str
    date_birthday: date
    bio: str
    skills: list[Skill] = field(default_factory=list)

    @property
    def correct_date_birthday(self) -> bool:
        return date(1900, 1, 1) <= self.date_birthday <= date.today()
