from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete

from app.db.session import get_db
from app.models.models import pulse, pulse_tags, tag
from app.schemas.pulse_schemas import CreatePulseAdmin, UpdatePulse, ChangeStatus
from app.api.role_checker import RoleChecker


router = APIRouter()

ALLOWED_CATEGORIES = ["project", "event"]


@router.put("/admin/pulse/{pulseID}/moderation")
def change_status(pulseID : int, request: Request, new_status: ChangeStatus,
                  session: Session = Depends(get_db),
                  role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    session.execute(update(pulse).values({"blocked": new_status.blocked}).where(pulse.c.id == pulseID))
    session.commit()


@router.get("/admin/pulses")
def all_pulses_admin(request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100,
                     session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    all_pulses = session.query(pulse).all()
    all_pulses_response = session.query(pulse).offset(skip).limit(limit).all()

    return {"remained": len(all_pulses) - len(all_pulses_response) - skip,
            "pulses": [{"id": i.id,
                        "name": i.name,
                        "created_at": i.created_at,
                        "blocked": i.blocked
                        } for i in all_pulses_response]}


@router.post("/admin/pulse")
async def create_pulse_admin(request: Request, new_pulse: CreatePulseAdmin,
                             session: Session = Depends(get_db),
                             role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    if new_pulse.category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=422, detail="Invalid category")

    new_pulse_tags = list(new_pulse.tags.split(","))
    for i in new_pulse_tags:
        tag_in_db_check = session.query(tag).where(tag.c.id == i).first()
        if not tag_in_db_check:
            raise HTTPException(status_code=422, detail="some tag is wrong from those that were sent")

    post_pulse = insert(pulse).values({"category": new_pulse.category,
                                        "name": new_pulse.name,
                                        "description": new_pulse.description,
                                        "short_description": new_pulse.short_description,
                                        "founder_id": new_pulse.user_id,
                                        }).returning(pulse.c.id)
    for row in session.execute(post_pulse):
        row_id = row.id

    for i in new_pulse_tags:
        new_pr_tag = insert(pulse_tags).values({"pulse_id": row_id,
                                                "tag_id": i})
        session.execute(new_pr_tag)
    session.commit()
    return {"pulse_id": row_id}


@router.put("/admin/pulse")
async def update_pulse_admin(request: Request, update_pulse: UpdatePulse,
                             session: Session = Depends(get_db),
                             role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    if update_pulse.category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=422, detail="Invalid category")

    new_tags = update_pulse.tags.split(",")

    pulse_update = update(pulse).values({"category": update_pulse.category,
                                         "name": update_pulse.name,
                                         "description": update_pulse.description,
                                         "short_description": update_pulse.short_description}).where(pulse.c.id == update_pulse.id)
    
    session.execute(pulse_update)

    session.execute(delete(pulse_tags).where(pulse_tags.c.pulse_id == update_pulse.id))
    for new_tag in new_tags:
        session.execute(insert(pulse_tags).values({"pulse_id": update_pulse.id, "tag_id": new_tag}))

    session.commit()
