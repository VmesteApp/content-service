from fastapi import APIRouter, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update
from app.models.models import complaints, pulse, notification
from app.schemas.complaint_schemas import CreateComplaint, VerdictComplaint
from app.api.role_checker import RoleChecker
from app.vk_session import vk
from app.gRPC.client import run


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
def all_complaints(request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)      
    all_comp = session.query(complaints).all()    
    all_complaints = session.query(complaints).offset(skip).limit(limit).all()
    return {"remained": len(all_comp) - len(all_complaints) - skip,
            "complaints": 
                        [{"id": i.id,
                        "pulse_id" : i.pulse_id,
                        "message": i.message,
                        "status": i.status
                        } for i in all_complaints]}


@router.put("/complaints/{complaintID}/verdict")
async def update_complaint(request: Request, complaintID: int, verdict: VerdictComplaint, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    up_complaint = update(complaints)
    if verdict.verdict == "APPROVED":
        pulse_id = session.query(complaints.c.pulse_id).where(complaints.c.id == complaintID).scalar_subquery()
        vals_compl = up_complaint.values({"status": verdict.verdict})
        up_pulse_block = update(pulse)
        session.execute(vals_compl.where(complaints.c.id == complaintID))
        vals_pilse = up_pulse_block.values({"blocked": True})
        session.execute(vals_pilse.where(pulse_id == pulse.c.id))
        pulse_name = session.query(pulse.c.name).where(pulse.c.id == pulse_id).first()
        uid = session.query(pulse.c.founder_id).where(pulse.c.id == pulse_id).first()[0]
        vk_id = run(uid)
        mes = f"Ваш импульс {pulse_name[0]} был заблокирован"
        print(vk_id)
        response = vk.notifications.sendMessage(
        user_ids = [vk_id],
        message = mes,
        title='Новое уведомление',
        button='Перейти в приложение'
        )
        session.execute(insert(notification).values({"user_id": uid,
                                                 "text": mes}))
        session.commit()
    else:
        vals_compl = up_complaint.values({"status": verdict.verdict})
        session.execute(vals_compl.where(complaints.c.id == complaintID))
    session.commit()
