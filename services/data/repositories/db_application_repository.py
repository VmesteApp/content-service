from typing import List

from sqlalchemy import insert, update, delete, select, or_, and_
from services.data.models.pulse_model import PulseORM as pulses_table
from services.data.models.pulse_tags_model import PulseTagsModelORM as pulse_tags_table
from services.data.models.pulse_members_model import PulseMembersModelORM as pulse_members_table
from services.data.models.application_model import ApplicationModelORM as applications_table
from services.data.models.image_model import ImageModelORM as images_table
from services.data.models.tag_model import TagModelORM as tags_table

from src.domain.entities.application import Application
from src.domain.interfaces.application_repository import ApplicationRepository


class DataBaseApplicationRepository(ApplicationRepository):
    def __init__(self, db_session) -> None:
        self.session = db_session

    def create_application(self, user_id: int, application: Application):
        # TODO Exeptions

        post_application = insert(application).values({"pulse_id": application.pulse_id,
                                                       "message": application.message,
                                                       "candidate_id": user_id,
                                                       })
        self.session.execute(post_application)
        self.session.commit()
        #TODO: return {"id":}

    def update_application(self, id: int, application: Application):
        pulse_candidate = self.session.query(applications_table.pulse_id, applications_table.candidate_id).where(applications_table.id == id).first()
        already_in_pulse_members_check = (self.session.query(pulse_members_table)
                                          .where((pulse_members_table.user_id == pulse_candidate.candidate_id) &
                                                 (pulse_members_table.pulse_id == pulse_candidate.pulse_id)).first())

        if application.status == "APPROVED":
            new_member = insert(pulse_members_table).values({"pulse_id": pulse_candidate.pulse_id,
                                                             "user_id": pulse_candidate.candidate_id
                                                             })
            self.session.execute(new_member)
            self.session.commit()       
  
        cond = update(application).values({"status": application.status}).where(applications_table.id == id)
        self.session.execute(cond)
        self.session.commit()

    def get_application_by_pulse_id(self, pulse_id: int):
        result = self.session.query(applications_table).where(applications_table.pulse_id == pulse_id)
        response = Application()
        return {"application": [{"pulse_id": i.pulse_id,
                                "candidate_id": i.candidate_id,
                                "id": i.id,
                                "message": i.message,
                                "status": i.status} for i in result]}

    def get_applications_by_user_id(self, user_id: int):

        images_query = self.session.query(images_table.image_path).where(images_table.pulse_id == user_id).all()

        response_query = (self.session.query(applications_table.id, applications_table.message, applications_table.status,
                                             pulses_table.id, pulses_table.name, pulses_table.category,
                                             pulses_table.description, pulses_table.short_description)
                                             .join(pulses_table, pulses_table.id == applications_table.pulse_id)
                                             .where(applications_table.candidate_id == user_id).all())

        for pulse_application in response_query:
            for images_for_pulse in images_query:
                if images_for_pulse.pulse_id == pulse_application.pulse_id:
                    pulse_application.append(images_for_pulse.image_path)

        return {"application": [
            {
                "pulse": {
                    "pulse_id": i.id,
                    "name": i.name,
                    "category": i.category,
                    "description": i.description,
                    "short_description": i.short_description,
                    "images": [j[3] for j in self.session.query(images_table).where(images_table.pulse_id == i.id).all()],
                    },
                "id": i.id,
                "message": i.message,
                "status": i.status
            } for i in response_query
        ]}
