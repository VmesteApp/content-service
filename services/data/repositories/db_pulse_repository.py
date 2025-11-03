from typing import List

from sqlalchemy import insert, update, delete, select, or_, and_
from services.data.models.pulse_model import PulseORM as pulses_table
from services.data.models.pulse_tags_model import PulseTagsModelORM as pulse_tags_table
from services.data.models.pulse_members_model import PulseMembersModelORM as pulse_members_table
from services.data.models.application_model import ApplicationModelORM as applications_table
from services.data.models.image_model import ImageModelORM as images_table
from services.data.models.tag_model import TagModelORM as tags_table

from src.domain.entities.pulse import Pulse
from src.domain.interfaces.pulse_repository import PulseRepository


class DataBasePulseRepository(PulseRepository):
    def __init__(self, db_session) -> None:
        self.session = db_session

    def create_pulse(self, pulse: Pulse) -> int:
        post_pulse = insert(pulses_table).values({"category": pulse.category,
                                                  "name": pulse.name,
                                                  "description": pulse.description,
                                                  "short_description": pulse.short_description,
                                                  "founder_id": pulse.founder_id,
                                                  }).returning(pulses_table.id)
        for row in self.session.execute(post_pulse):
            row_id = row.id
        new_pulse_tags = list(pulse.tags.split(","))
        for i in new_pulse_tags:
            new_pr_tag = insert(pulse_tags_table).values({"pulse_id":  row_id,
                                                          "tag_id": i})
            self.session.execute(new_pr_tag)
        self.session.commit()
        return row_id

    def update_pulse(self, pulse: Pulse) -> bool:
        pulse_update = update(pulse).values({"category": pulse.category,
                                             "name": pulse.name,
                                             "description": pulse.description,
                                             "short_description": pulse.short_description
                                             }).where(pulse.c.id == pulse.id)
        
        self.session.execute(pulse_update)
        self.session.execute(delete(pulse_tags_table).where(pulse_tags_table.pulse_id == pulse.id))

        new_tags = pulse.tags.split(",")
        for new_tag in new_tags:
            self.session.execute(insert(pulse_tags_table).values({"pulse_id": pulse.id,
                                                                  "tag_id": new_tag}))

        self.session.commit()

    def delete_pulse(self, id: int) -> bool:
        self.session.execute(delete(pulses_table).where(id == pulses_table.id))
        self.session.execute(delete(pulse_tags_table).where(id == pulse_tags_table.pulse_id))
        self.session.execute(delete(pulse_members_table).where(id == pulse_members_table.pulse_id))
        self.session.execute(delete(applications_table).where(id == applications_table.pulse_id))
        self.session.commit()

    def get_all_pulses(self, user_id: int) -> List[Pulse]:
        project_members_subquery = (select(pulse_members_table.pulse_id)
                                    .where(pulse_members_table.user_id == user_id))

        query = (select(pulses_table).where(and_(or_(pulses_table.founder_id == user_id,
                                                     pulses_table.id.in_(project_members_subquery)),
                                                     pulses_table.blocked.isnot(True))))
        
        res = self.session.execute(query).scalars().all()

        response = [Pulse(
            id=pulse.id,
            category=pulse.category,
            name=pulse.name,
            founder_id=pulse.founder_id,
            description=pulse.description,
            short_description=pulse.short_description,
            blocked=pulse.blocked,
            images=[j[3] for j in self.session.query(images_table).where(images_table.pulse_id == pulse.id).all()],
            members=None,
            tags=None
            ) for pulse in res]

        return response

    def get_pulse(self, pulse_id: int) -> Pulse:
        pulse = self.session.query(pulses_table).where(pulses_table.id == pulse_id).first()

        members = self.session.query(pulse_members_table.user_id).where(pulse_members_table.pulse_id == pulse_id).all()
        images_query = self.session.query(images_table.image_path).where(images_table.pulse_id == pulse_id).all()
        tags = (self.session.query(pulse_tags_table.pulse_id, tags_table.id, tags_table.name)
                .join(tags_table, tags_table.id == pulse_tags_table.tag_id)
                .where(pulse_tags_table.pulse_id == pulse_id).all())

        response = Pulse(
            id=pulse.id,
            category=pulse.category,
            name=pulse.name,
            founder_id=pulse.founder_id,
            description=pulse.description,
            short_description=pulse.short_description,
            blocked=pulse.blocked,
            images=[image.image_path for image in images_query],
            members=[member.user_id for member in members],
            tags=[{'id': i.id, 'name': i.name} for i in tags]
            )
        
        return response
