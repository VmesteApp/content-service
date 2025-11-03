from typing import List, Optional
from sqlalchemy import insert, update, select
from sqlalchemy.orm import Session

from services.data.models.complaint_model import ComplaintModelORM as complaints_table
from services.data.models.pulse_model import PulseORM as pulses_table
from services.data.models.notification_model import NotificationModelORM as notifications_table

from src.domain.entities.complaint import Complaint
from src.domain.dto.complaint_dto.get_complaints import GetComplaintsOutputDto
from src.domain.interfaces.complaint_repository import ComplaintRepository


class DataBaseComplaintRepository(ComplaintRepository):
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def create_complaint(self, complaint: Complaint) -> bool:
        try:
            stmt = insert(complaints_table).values({
                "pulse_id": complaint.pulse_id,
                "message": complaint.message,
                "status": complaint.status
            })
            self.session.execute(stmt)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_all_complaints(self) -> List[GetComplaintsOutputDto]:
        try:
            stmt = select(complaints_table)
            complaints = self.session.execute(stmt).scalars().all()
            
            return [
                GetComplaintsOutputDto(
                    id=complaint.id,
                    pulse_id=complaint.pulse_id,
                    message=complaint.message,
                    status=complaint.status
                )
                for complaint in complaints
            ]
        except Exception:
            raise

    def update_complaint_status(self, complaint_id: int, status: str) -> bool:
        try:
            stmt = (
                update(complaints_table)
                .where(complaints_table.id == complaint_id)
                .values({"status": status})
            )
            self.session.execute(stmt)
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_complaint_details(self, complaint_id: int) -> Optional[dict]:
        try:
            stmt = select(complaints_table).where(complaints_table.id == complaint_id)
            complaint = self.session.execute(stmt).scalar_one_or_none()
            
            if complaint:
                return {
                    "pulse_id": complaint.pulse_id,
                    "message": complaint.message
                }
            return None
        except Exception:
            raise

    def block_pulse(self, pulse_id: int) -> bool:
        try:
            stmt = (
                update(pulses_table)
                .where(pulses_table.id == pulse_id)
                .values({"blocked": True})
            )
            self.session.execute(stmt)
            return True
        except Exception:
            self.session.rollback()
            raise

    def create_notification(self, user_id: int, text: str) -> bool:
        try:
            stmt = insert(notifications_table).values({
                "user_id": user_id,
                "text": text
            })
            self.session.execute(stmt)
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_pulse_founder_id(self, pulse_id: int) -> Optional[int]:
        try:
            stmt = select(pulses_table.founder_id).where(pulses_table.id == pulse_id)
            return self.session.execute(stmt).scalar_one_or_none()
        except Exception:
            raise

    def get_pulse_name(self, pulse_id: int) -> Optional[str]:
        try:
            stmt = select(pulses_table.name).where(pulses_table.id == pulse_id)
            return self.session.execute(stmt).scalar_one_or_none()
        except Exception:
            raise
