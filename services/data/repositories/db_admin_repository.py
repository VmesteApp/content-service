from typing import List
from sqlalchemy import update, delete, insert, select
from sqlalchemy.orm import Session

from services.data.models.pulse_model import PulseORM as pulses_table
from services.data.models.pulse_tags_model import PulseTagsModelORM as pulse_tags_table
from services.data.models.tag_model import TagModelORM as tags_table

from src.domain.entities.pulse import Pulse
from src.domain.dto.admin_dto.get_all_pulses import GetAllPulsesOutputDto
from src.domain.interfaces.admin_repository import AdminRepository


class DataBaseAdminRepository(AdminRepository):
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def change_pulse_status(self, pulse_id: int, blocked: bool) -> bool:
        try:
            stmt = (
                update(pulses_table)
                .where(pulses_table.id == pulse_id)
                .values({"blocked": blocked})
            )
            self.session.execute(stmt)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_all_pulses(self, skip: int, limit: int) -> List[GetAllPulsesOutputDto]:
        try:
            stmt = (
                select(pulses_table)
                .offset(skip)
                .limit(limit)
                .order_by(pulses_table.created_at.desc())
            )
            
            pulses = self.session.execute(stmt).scalars().all()
            
            return [
                GetAllPulsesOutputDto(
                    id=pulse.id,
                    name=pulse.name,
                    created_at=pulse.created_at.isoformat(),
                    blocked=pulse.blocked
                )
                for pulse in pulses
            ]
        except Exception:
            raise

    def create_pulse_admin(self, pulse: Pulse, tags_str: str) -> int:
        try:
            stmt = (
                insert(pulses_table)
                .values({
                    "category": pulse.category,
                    "name": pulse.name,
                    "description": pulse.description,
                    "short_description": pulse.short_description,
                    "founder_id": pulse.founder_id,
                })
                .returning(pulses_table.id)
            )
            
            result = self.session.execute(stmt)
            pulse_id = result.scalar_one()
            
            if tags_str:
                tag_ids = [int(tag.strip()) for tag in tags_str.split(",") if tag.strip().isdigit()]
                tag_values = [{"pulse_id": pulse_id, "tag_id": tag_id} for tag_id in tag_ids]
                
                if tag_values:
                    self.session.execute(insert(pulse_tags_table), tag_values)
            
            self.session.commit()
            return pulse_id
            
        except Exception:
            self.session.rollback()
            raise

    def update_pulse_admin(self, pulse: Pulse, tags_str: str) -> bool:
        try:
            stmt = (
                update(pulses_table)
                .where(pulses_table.id == pulse.id)
                .values({
                    "category": pulse.category,
                    "name": pulse.name,
                    "description": pulse.description,
                    "short_description": pulse.short_description,
                })
            )
            self.session.execute(stmt)
            
            self.session.execute(
                delete(pulse_tags_table).where(pulse_tags_table.pulse_id == pulse.id)
            )
            
            if tags_str:
                tag_ids = [int(tag.strip()) for tag in tags_str.split(",") if tag.strip().isdigit()]
                tag_values = [{"pulse_id": pulse.id, "tag_id": tag_id} for tag_id in tag_ids]
                
                if tag_values:
                    self.session.execute(insert(pulse_tags_table), tag_values)
            
            self.session.commit()
            return True
            
        except Exception:
            self.session.rollback()
            raise

    def check_tag_exists(self, tag_id: int) -> bool:
        try:
            stmt = select(tags_table.id).where(tags_table.id == tag_id)
            return self.session.execute(stmt).scalar_one_or_none() is not None
        except Exception:
            raise
