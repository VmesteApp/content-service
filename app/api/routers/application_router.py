from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, select
from app.models.models import application, pulse_members
from app.schemas.applications_schemas import SendApplication, Verdict
from app.api.role_checker import RoleChecker


router = APIRouter()


@router.post("/application")
async def create_application(request: Request, new_application: SendApplication,  session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    post_application = insert(application).values({"pulse_id": new_application.pulse_id,
                                                   "message": new_application.message,
                                                    "candidate_id": request.state.uid,
                                                    })
    session.execute(post_application)
    session.commit()





@router.put("/application/verdict")
async def update_application(request: Request, verdict: Verdict, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    appli = update(application)
    if verdict.status == "APPROVED":
        new_member = insert(pulse_members).values({"pulse_id": verdict.pulse_id,
                                                   "user_id": verdict.candidate_id,
                                                    })
        session.execute(new_member)
        session.commit()
    val = appli.values({"status": verdict.status})
    cond = val.where((application.c.pulse_id == verdict.pulse_id) & (application.c.candidate_id == verdict.candidate_id))
    session.execute(cond)
    session.commit()


@router.get("/application/{pulse_id}")
def find_application(pulse_id: int, request: Request, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    result = session.query((application)).where(application.c.pulse_id == pulse_id)
    return {"application": [{"pulse_id": i.pulse_id, "candidate_id": i.candidate_id, "message": i.message, "status": i.status} for i in result]}


@router.get("/applications/{candidate_id}")
def find_application(candidate_id: int, request: Request, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    result = session.query((application)).where(application.c.candidate_id == candidate_id)
    return {"application": [{"pulse_id": i.pulse_id, "candidate_id": i.candidate_id, "message": i.message, "status": i.status} for i in result]}
