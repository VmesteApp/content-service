from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, select
from app.models.models import application, pulse_members, pulse, images, pulse_tags, tag
from app.schemas.applications_schemas import SendApplication, Verdict
from app.api.role_checker import RoleChecker


router = APIRouter()


@router.post("/application")
async def create_application(request: Request, new_application: SendApplication, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    already_in_applications_check = session.query(application).where((application.c.candidate_id == request.state.uid) & (application.c.pulse_id == new_application.pulse_id)).first()
    if already_in_applications_check:
        return {"this user already in applications for this pulse"}
    existence_pulse_check = session.query(pulse).where(pulse.c.id == new_application.pulse_id).first()
    if not existence_pulse_check:
        return {"there is no pulse with this id"}
    already_in_pulse_members_check = session.query(pulse_members).where((pulse_members.c.user_id == request.state.uid) & (pulse_members.c.pulse_id == new_application.pulse_id)).first()
    if already_in_pulse_members_check:
        return {"this user already in members of this project"}
    post_application = insert(application).values({"pulse_id": new_application.pulse_id,
                                                   "message": new_application.message,
                                                   "candidate_id": request.state.uid,
                                                  })
    session.execute(post_application)
    session.commit()


@router.put("/application/{id}/verdict")
async def update_application(request: Request, id: int, verdict: Verdict, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    already_in_application_table_check = session.query(application).where(application.c.id == id).first()
    if already_in_application_table_check:
        pulse_candidate = session.query(application.c.pulse_id, application.c.candidate_id).where(application.c.id == id).first()
        already_in_pulse_members_check = (session.query(pulse_members)
                                          .where((pulse_members.c.user_id == pulse_candidate.candidate_id) &
                                                 (pulse_members.c.pulse_id == pulse_candidate.pulse_id)).first())
        if already_in_pulse_members_check:
            return {"this user already in members of this project"}
        if verdict.status == "APPROVED":
            new_member = insert(pulse_members).values({"pulse_id": pulse_candidate.pulse_id,
                                                       "user_id": pulse_candidate.candidate_id
                                                       })
            session.execute(new_member)
            session.commit()            
        cond = update(application).values({"status": verdict.status}).where(application.c.id == id)
        session.execute(cond)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="there is no application with this id")


@router.get("/application/{pulse_id}")
def find_application(pulse_id: int, request: Request, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    result = session.query(application).where(application.c.pulse_id == pulse_id)
    return {"application": [{"pulse_id": i.pulse_id,
                             "candidate_id": i.candidate_id,
                             "id": i.id,
                             "message": i.message,
                             "status": i.status} for i in result]}


@router.get("/application/my/")
def find_application(request: Request, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    response_query = (session.query(application.c.id, application.c.message, application.c.status, pulse.c.id, pulse.c.name,
                                    pulse.c.category, pulse.c.description, pulse.c.short_description)
                                    .join(pulse, pulse.c.id == application.c.pulse_id)
                                    .where(application.c.candidate_id == request.state.uid).all())

    return {"application": [
        {
            "pulse": {
                "pulse_id": i.id,
                "name": i.name,
                "category": i.category,
                "description": i.description,
                "short_description": i.short_description,
                "images": [j[2] for j in session.query(images).where(images.c.pulse_id == i.id).all()],
                },
            "id": i.id,
            "message": i.message,
            "status": i.status
        } for i in response_query
    ]}
