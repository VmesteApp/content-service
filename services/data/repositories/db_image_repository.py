import os
from typing import Optional
from uuid import UUID
from sqlalchemy import insert, delete, select, func
from sqlalchemy.orm import Session

from services.data.models.image_model import ImageModelORM as images_table
from services.data.models.pulse_model import PulseORM as pulses_table
from services.data.models.pulse_members_model import PulseMembersModelORM as pulse_members_table

from src.domain.entities.image import Image
from src.domain.interfaces.image_repository import ImageRepository


class DataBaseImageRepository(ImageRepository):
    def __init__(self, db_session: Session, upload_files_dir: str = 'uploaded_files') -> None:
        self.session = db_session
        self.upload_files_dir = upload_files_dir
        os.makedirs(upload_files_dir, exist_ok=True)

    def _get_file_path(self, filename: str) -> str:
        return os.path.join(self.upload_files_dir, filename)

    def create_image(self, image: Image) -> bool:
        try:
            stmt = insert(images_table).values({
                "image_id": image.image_id,
                "pulse_id": image.pulse_id,
                "full_name": image.full_name,
                "image_path": image.image_path
            })
            self.session.execute(stmt)
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_image_path(self, image_uuid: UUID) -> Optional[str]:
        try:
            stmt = select(images_table.full_name).where(images_table.image_id == image_uuid)
            result = self.session.execute(stmt).scalar_one_or_none()
            return self._get_file_path(result) if result else None
        except Exception:
            raise

    def delete_image(self, image_uuid: UUID) -> bool:
        try:
            stmt_select = select(images_table.full_name).where(images_table.image_id == image_uuid)
            filename = self.session.execute(stmt_select).scalar_one_or_none()
            
            if filename:
                file_path = self._get_file_path(filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            stmt_delete = delete(images_table).where(images_table.image_id == image_uuid)
            self.session.execute(stmt_delete)
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_images_count(self, pulse_id: int) -> int:
        try:
            stmt = select(func.count()).select_from(images_table).where(images_table.pulse_id == pulse_id)
            return self.session.execute(stmt).scalar()
        except Exception:
            raise

    def check_pulse_exists(self, pulse_id: int) -> bool:
        try:
            stmt = select(pulses_table.id).where(pulses_table.id == pulse_id)
            return self.session.execute(stmt).scalar_one_or_none() is not None
        except Exception:
            raise

    def check_image_exists(self, image_uuid: UUID) -> bool:
        try:
            stmt = select(images_table.image_id).where(images_table.image_id == image_uuid)
            return self.session.execute(stmt).scalar_one_or_none() is not None
        except Exception:
            raise

    def check_user_has_access(self, pulse_id: int, user_id: int) -> bool:
        try:
            stmt_founder = select(pulses_table.id).where(
                pulses_table.id == pulse_id,
                pulses_table.founder_id == user_id
            )
            
            stmt_member = select(pulse_members_table.pulse_id).where(
                pulse_members_table.pulse_id == pulse_id,
                pulse_members_table.user_id == user_id
            )
            
            is_founder = self.session.execute(stmt_founder).scalar_one_or_none() is not None
            is_member = self.session.execute(stmt_member).scalar_one_or_none() is not None
            
            return is_founder or is_member
        except Exception:
            raise
