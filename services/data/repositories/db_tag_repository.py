from typing import List
from sqlalchemy import insert, update, delete, select
from sqlalchemy.orm import Session

from services.data.models.tag_model import TagModelORM as tags_table
from services.data.models.pulse_tags_model import PulseTagsModelORM as pulse_tags_table

from src.domain.entities.tag import Tag
from src.domain.interfaces.tag_repository import TagRepository


class DataBaseTagRepository(TagRepository):
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def create_tag(self, tag: Tag) -> int:
        try:
            stmt = insert(tags_table).values({"name": tag.name}).returning(tags_table.id)
            result = self.session.execute(stmt)
            tag_id = result.scalar_one()
            self.session.commit()
            return tag_id
        except Exception as error:
            self.session.rollback()
            raise Exception(f"Failed to create tag: {str(error)}")

    def update_tag(self, tag: Tag) -> bool:
        try:
            stmt = (
                update(tags_table)
                .where(tags_table.id == tag.id)
                .values({"name": tag.name})
            )
            self.session.execute(stmt)
            self.session.commit()
            return True
        except Exception as error:
            self.session.rollback()
            raise Exception(f"Failed to update tag: {str(error)}")

    def delete_tag(self, tag_id: int) -> bool:
        try:
            self.session.execute(
                delete(pulse_tags_table).where(pulse_tags_table.tag_id == tag_id)
            )
            
            self.session.execute(
                delete(tags_table).where(tags_table.id == tag_id)
            )
            
            self.session.commit()
            return True
        except Exception as error:
            self.session.rollback()
            raise Exception(f"Failed to delete tag: {str(error)}")

    def get_all_tags(self) -> List[Tag]:
        try:
            stmt = select(tags_table)
            result = self.session.execute(stmt).scalars().all()
            
            return [
                Tag(id=tag.id, name=tag.name)
                for tag in result
            ]
        except Exception as error:
            raise Exception(f"Failed to get tags: {str(error)}")
