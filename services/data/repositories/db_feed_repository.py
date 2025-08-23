from typing import List
from sqlalchemy import select, not_, and_, or_
from sqlalchemy.orm import Session

from services.data.models.pulse_model import PulseORM as pulses_table
from services.data.models.pulse_members_model import PulseMembersModelORM as pulse_members_table
from services.data.models.image_model import ImageModelORM as images_table
from services.data.models.pulse_tags_model import PulseTagsModelORM as pulse_tags_table
from services.data.models.tag_model import TagModelORM as tags_table

from src.domain.entities.feed import FeedItem
from src.domain.dto.feed_dto.get_feed import GetFeedInputDto
from src.domain.interfaces.feed_repository import FeedRepository


class DataBaseFeedRepository(FeedRepository):
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def get_feed_items(self, dto: GetFeedInputDto) -> List[FeedItem]:
        pulse_members_subquery = (
            select(pulse_members_table.pulse_id)
            .where(pulse_members_table.user_id == dto.user_id)
        )

        query = (
            select(pulses_table)
            .where(
                not_(pulses_table.founder_id == dto.user_id),
                not_(pulses_table.id.in_(pulse_members_subquery)),
                pulses_table.blocked.isnot(True)
            )
            .offset(dto.skip)
            .limit(dto.limit)
        )

        if dto.tags:
            tagged_pulses_subquery = (
                select(pulse_tags_table.pulse_id)
                .where(pulse_tags_table.tag_id.in_(dto.tags))
                .distinct()
            )
            query = query.where(pulses_table.id.in_(tagged_pulses_subquery))

        if dto.name:
            query = query.where(pulses_table.name.ilike(f"%{dto.name}%"))

        pulses = self.session.execute(query).scalars().all()

        all_tags = {}
        if pulses:
            pulse_ids = [pulse.id for pulse in pulses]
            tags_query = (
                self.session.query(
                    pulse_tags_table.pulse_id,
                    tags_table.id,
                    tags_table.name
                )
                .join(tags_table, tags_table.id == pulse_tags_table.tag_id)
                .where(pulse_tags_table.pulse_id.in_(pulse_ids))
            )
            for tag in tags_query:
                if tag.pulse_id not in all_tags:
                    all_tags[tag.pulse_id] = []
                all_tags[tag.pulse_id].append({"id": tag.id, "name": tag.name})

        all_images = {}
        if pulses:
            images_query = (
                self.session.query(
                    images_table.pulse_id,
                    images_table.image_path
                )
                .where(images_table.pulse_id.in_(pulse_ids))
            )
            for image in images_query:
                if image.pulse_id not in all_images:
                    all_images[image.pulse_id] = []
                all_images[image.pulse_id].append(image.image_path)

        feed_items = []
        for pulse in pulses:
            feed_items.append(FeedItem(
                id=pulse.id,
                category=pulse.category,
                name=pulse.name,
                founder_id=pulse.founder_id,
                description=pulse.description,
                short_description=pulse.short_description,
                images=all_images.get(pulse.id, []),
                tags=all_tags.get(pulse.id, [])
            ))

        return feed_items
