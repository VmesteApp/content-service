from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select
from app.models.models import complaints, pulse
from app.schemas.сomplaint_schemas import CreateСomplaint, VerdictСomplaint
from app.api.role_checker import RoleChecker


router = APIRouter()


@router.post("/complaints/{pulseID}")
def create_complaint(request: Request, pulseID: int, new_complaint: CreateСomplaint, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    post_complaint = insert(complaints).values({"pulse_id": pulseID,
                                        "message": new_complaint.message,
                                        })
    session.execute(post_complaint)
    session.commit()


@router.get("/complaints")
def all_complaints(request: Request, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)          
    all_complaints = session.query(complaints).where()
    print(63263723)
    return {"complaints": [{"id": i.id,
                        "pulse_id" : i.pulse_id,
                        "message": i.message,
                        "status": i.status
                        } for i in all_complaints]}


@router.put("/complaints/{pulseID}/verdict")
async def update_complaint(request: Request, pulseID: int, verdict: VerdictСomplaint, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    up_complaint = update(complaints)
    if verdict.verdict == "APPROVED":
        vals_compl = up_complaint.values({"status": verdict.verdict})
        up_pulse_block = update(pulse)
        session.execute(vals_compl.where(complaints.c.id == verdict.id))
        vals_pilse = up_pulse_block.values({"blocked": True})
        session.execute(vals_pilse.where(pulseID == pulse.c.id))
    else:
        vals_compl = up_complaint.values({"verdict": verdict.verdict})
        session.execute(vals_compl.where(complaints.c.id == verdict.id))
    session.commit()