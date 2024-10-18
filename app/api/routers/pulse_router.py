from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select
from app.models.models import pulse, pulse_tags, tag
from app.schemas.pulse_schemas import CreatePulse, UpdatePulse, DeletePulse


router = APIRouter()

ALLOWED_CATEGORIES = ["project", "event"]


@router.post("/pulse")
async def create_pulse(request: Request, new_pulse: CreatePulse, session: Session = Depends(get_db)):
    if request.state.role == "user":
        if new_pulse.category not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=422, detail="Invalid category")
        post_pulse = insert(pulse).values({"category": new_pulse.category,
                                           "name": new_pulse.name,
                                           "description": new_pulse.description,
                                           "short_description": new_pulse.short_description
                                           }).returning(pulse.c.id)
        for row in session.execute(post_pulse):
            row_id = row.id
        new_pulse_tags = list(new_pulse.tags.split(","))
        for i in new_pulse_tags:
            new_pr_tag = insert(pulse_tags).values({"pulse_id":  row_id,
                                                    "tag_id": i})
            session.execute(new_pr_tag)
        session.commit()
    else:
        raise HTTPException(status_code=403, detail="Invalid role type")


@router.put("/pulse")
async def update_pulse(request: Request, update_pulse: UpdatePulse, session: Session = Depends(get_db)):
    if request.state.role == "user":
        if update_pulse.category not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=422, detail="Invalid category")
        new_tagss = []
        pulse_up = update(pulse)
        val = pulse_up.values({"category": update_pulse.category,
                               "name": update_pulse.name,
                               "description": update_pulse.description,
                               "short_description": update_pulse.short_description})
        cond = val.where(pulse.c.id == update_pulse.id)
        session.execute(cond)
        update_tags = list(update_pulse.tags.split(","))
        tags_id_old = session.execute(select(pulse_tags.c.tag_id)
                                      .where(update_pulse.id == pulse_tags.c.pulse_id)).scalars().all()
        for i in update_tags:
            tag_id = session.execute(select(tag).where(tag.c.name == i)).scalar()
            new_tagss.append(tag_id)
            if tag_id not in tags_id_old:
                new_pr_tag = insert(pulse_tags).values({"pulse_id": update_pulse.id,
                                                        "tag_id": tag_id})
                session.execute(new_pr_tag)
        for j in tags_id_old:
            if j not in new_tagss:
                result = session.execute(delete(pulse_tags)
                                         .where((pulse_tags.c.tag_id == j) &
                                                (update_pulse.id == pulse_tags.c.pulse_id)))
        session.commit()
    else:
        raise HTTPException(status_code=403, detail="Invalid role type")


@router.delete("/pulse")
def delte_pulse(request: Request, delete_pulse: DeletePulse, session: Session = Depends(get_db)):
    if request.state.role == "user":
        result = session.execute(delete(pulse).where(delete_pulse.id == pulse.c.id))
        session.execute(delete(pulse_tags).where(delete_pulse.id == pulse_tags.c.pulse_id))
        session.commit()
    else:
        raise HTTPException(status_code=403, detail="Invalid role type")


@router.get("/pulses")
def all_pulse(session: Session = Depends(get_db)):
    pulses = session.query((pulse)).all()
    return {"pulses": [list(pulse_1) for pulse_1 in pulses]}


@router.get("/pulses/{pulse_id}")
def find_pulse(pulse_id: int, session: Session = Depends(get_db)):
    result = session.query(pulse).where(pulse.c.id == pulse_id).all()
    return {
            "status": "success",
            "data": [list(pulse_1) for pulse_1 in result],
            "details": None
        }
