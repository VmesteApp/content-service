from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select
from app.models.models import pulse, pulse_tags, tag, pulse_members, images
from app.schemas.pulse_schemas import CreatePulse, UpdatePulse
from app.api.role_checker import RoleChecker


router = APIRouter()

ALLOWED_CATEGORIES = ["project", "event"]


@router.post("/pulse")
async def create_pulse(request: Request, new_pulse: CreatePulse , session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    if new_pulse.category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=422, detail="Invalid category")
    post_pulse = insert(pulse).values({"category": new_pulse.category,
                                        "name": new_pulse.name,
                                        "description": new_pulse.description,
                                        "short_description": new_pulse.short_description,
                                        "founder_id": request.state.uid,
                                        }).returning(pulse.c.id)
    for row in session.execute(post_pulse):
        row_id = row.id
    new_pulse_tags = list(new_pulse.tags.split(","))
    for i in new_pulse_tags:
        new_pr_tag = insert(pulse_tags).values({"pulse_id":  row_id,
                                                "tag_id": i})
        session.execute(new_pr_tag)
    session.commit()
    return {"pulse_id": row_id}


@router.put("/pulse")
async def update_pulse(request: Request, update_pulse: UpdatePulse, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
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
            session.execute(delete(pulse_tags)
                                    .where((pulse_tags.c.tag_id == j) &
                                        (update_pulse.id == pulse_tags.c.pulse_id)))
    session.commit()


@router.delete("/pulse/{delete_pulse}")
def delete_pulse(request: Request, delete_pulse: int, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    session.execute(delete(pulse).where(delete_pulse == pulse.c.id))
    session.execute(delete(pulse_tags).where(delete_pulse == pulse_tags.c.pulse_id))
    session.commit()


@router.get("/pulses")
def all_pulses(request: Request, session: Session = Depends(get_db)):
    pulses_members_query = (select(pulse)
                           .join(pulse_members, pulse_members.c.pulse_id == pulse.c.id)
                           .where(pulse_members.c.pulse_id.isnot(None)))

    pulses_founders_query = (select(pulse)
                             .where(pulse.c.founder_id == request.state.uid))

    pulses_members = session.execute(pulses_members_query).all()
    pulses_founders = session.execute(pulses_founders_query).all()
    tags = session.query((tag)).all()

    all_user_pulses = set()
    for one_pulse in pulses_members:
        all_user_pulses.add(one_pulse)

    for one_pulse in pulses_founders:
        all_user_pulses.add(one_pulse)

    return {"pulses": [{"id": i.id,
                        "category" : i.category,
                        "name": i.name,
                        "founder_id": i.founder_id,
                        "description": i.description,
                        "short_description": i.short_description,
                        "images": [j[3] for j in session.query(images).where(images.c.pulse_id == i.id).all()],
                        "tags": [{"id": i.id, "name": i.name} for i in tags]
                        } for i in all_user_pulses]}


@router.get("/pulses/{pulse_id}")
def find_pulse(pulse_id: int, session: Session = Depends(get_db)):
    result = session.query(pulse).where(pulse.c.id == pulse_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="There is no pulse with this id")
    members = session.query(pulse_members.c.user_id).where(pulse_members.c.pulse_id == pulse_id).all()
    images_query = session.query(images.c.image_path).where(images.c.pulse_id == pulse_id).all()
    tags = session.query((tag)).all()
    return {"id": result.id,
            "category": result.category,
            "name": result.name,
            "founder_id": result.founder_id,
            "description": result.description,
            "short_description": result.short_description,
            "members": [member.user_id for member in members],
            "images": [image.image_path for image in images_query],
            "tags": [{"id": i.id, "name": i.name} for i in tags]
            }
