from fastapi import APIRouter, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update
from app.models.models import complaints, pulse
from app.schemas.complaint_schemas import CreateComplaint, VerdictComplaint
from app.api.role_checker import RoleChecker


router = APIRouter()


@router.post("/pulses/{pulseID}/complaint")
def create_complaint(request: Request, pulseID: int, new_complaint: CreateComplaint, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    post_complaint = insert(complaints).values({"pulse_id": pulseID,
                                        "message": new_complaint.message,
                                        })
    session.execute(post_complaint)
    session.commit()


@router.get("/complaints")
def all_complaints(request: Request, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)          
    all_complaints = session.query(complaints).all()
    return {"complaints": [{"id": i.id,
                        "pulse_id" : i.pulse_id,
                        "message": i.message,
                        "status": i.status
                        } for i in all_complaints]}


@router.put("/complaints/{complaintID}/verdict")
async def update_complaint(request: Request, complaintID: int, verdict: VerdictComplaint, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    up_complaint = update(complaints)

    if verdict.verdict == "APPROVED":
        pulse_id = session.query(complaints.c.pulse_id).where(complaints.c.id == complaintID).all()
        vals_compl = up_complaint.values({"status": verdict.verdict})
        up_pulse_block = update(pulse)
        session.execute(vals_compl.where(complaints.c.id == complaintID))
        vals_pilse = up_pulse_block.values({"blocked": True})
        session.execute(vals_pilse.where(pulse_id == pulse.c.id))
    else:
        vals_compl = up_complaint.values({"verdict": verdict.verdict})
        session.execute(vals_compl.where(complaints.c.id == complaintID))
    session.commit()
