from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select, or_, and_
from app.models.models import pulse, pulse_tags, tag, pulse_members, images, application
from app.schemas.pulse_schemas import CreatePulse, UpdatePulse, ChangeStatus
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


@router.delete("/pulse/{delete_pulse}")
def delete_pulse(request: Request, delete_pulse: int, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    founder = session.query(pulse.c.founder_id).where(pulse.c.id == delete_pulse).first()[0]
    if founder == request.state.uid:
        session.execute(delete(pulse).where(delete_pulse == pulse.c.id))
        session.execute(delete(pulse_tags).where(delete_pulse == pulse_tags.c.pulse_id))
        session.execute(delete(pulse_members).where(delete_pulse == pulse_members.c.pulse_id))
        session.execute(delete(application).where(delete_pulse == application.c.pulse_id))
        session.execute(delete(images).where(delete_pulse == images.c.pulse_id))
        session.commit()
    else:
        return JSONResponse(status_code=403, content="Insufficient rights to delete the pulse")


@router.get("/pulses/my/")
def all_pulses(request: Request, session: Session = Depends(get_db)):

    project_members_subquery = (select(pulse_members.c.pulse_id).join(pulse, pulse.c.id == pulse_members.c.pulse_id)
                                .where(and_(pulse_members.c.user_id == request.state.uid, pulse.c.blocked.isnot(True))))

    query = (select(pulse).where(or_(pulse.c.founder_id == request.state.uid,
                                     pulse.c.id.in_(project_members_subquery))))
    
    res = session.execute(query).all()

    return {"pulses": [{"id": i.id,
                        "category" : i.category,
                        "name": i.name,
                        "founder_id": i.founder_id,
                        "description": i.description,
                        "short_description": i.short_description,
                        "blocked": i.blocked,
                        "images": [j.image_path for j in session.query(images).where(images.c.pulse_id == i.id).all()],
                        } for i in res]}


@router.get("/pulses/{pulse_id}")
def find_pulse(request: Request, pulse_id: int, session: Session = Depends(get_db)):
    result = session.query(pulse).where(pulse.c.id == pulse_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="There is no pulse with this id")
    members = session.query(pulse_members.c.user_id).where(pulse_members.c.pulse_id == pulse_id).all()
    membr = [i[0] for i in members]
    if request.state.uid not in membr and request.state.uid != result.founder_id:
        return JSONResponse(status_code=403, content={"message": "There are not enough rights"})
    images_query = session.query(images.c.image_path).where(images.c.pulse_id == pulse_id).all()
    tags = (session.query(pulse_tags.c.pulse_id, tag.c.id, tag.c.name)
            .join(tag, tag.c.id == pulse_tags.c.tag_id).
            where(pulse_tags.c.pulse_id == pulse_id).all())

    return {"id": result.id,
            "category": result.category,
            "name": result.name,
            "founder_id": result.founder_id,
            "description": result.description,
            "short_description": result.short_description,
            "members": [member.user_id for member in members],
            "blocked": result.blocked,
            "images": [image.image_path for image in images_query],
            "tags": [{"id": i.id, "name": i.name} for i in tags],
            "blocked": result.blocked,
            }


@router.get("/pulses/{pulse_id}/preview")
def find_pulse(request: Request, pulse_id: int, session: Session = Depends(get_db)):
    result = session.query(pulse).where(pulse.c.id == pulse_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="There is no pulse with this id")
    members = session.query(pulse_members.c.user_id).where(pulse_members.c.pulse_id == pulse_id).all()
    images_query = session.query(images.c.image_path).where(images.c.pulse_id == pulse_id).all()
    tags = (session.query(pulse_tags.c.pulse_id, tag.c.id, tag.c.name)
            .join(tag, tag.c.id == pulse_tags.c.tag_id).
            where(pulse_tags.c.pulse_id == pulse_id).all())

    return {"id": result.id,
            "category": result.category,
            "name": result.name,
            "description": result.description,
            "short_description": result.short_description,
            "blocked": result.blocked,
            "images": [image.image_path for image in images_query],
            "tags": [{"id": i.id, "name": i.name} for i in tags]
            }


@router.delete("/pulses/{pulseID}/members/{userID}")
def delete_user(pulseID : int, userID : int, request: Request, session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    founder = session.query(pulse.c.founder_id).where(pulse.c.id == pulseID).first()
    if founder == None:
        raise HTTPException(status_code=404, detail="There is no pulse with this id")
    if request.state.uid in founder:
        session.execute(delete(pulse_members).where(and_(pulse_members.c.pulse_id == pulseID, pulse_members.c.user_id == userID)))
        session.commit()
    else:
        return JSONResponse(status_code=403, content="There are not enough rights to delete the user from this pulse")


@router.put("/admin/pulse/{pulseID}/moderation")
def change_status(pulseID : int, request: Request, new_status: ChangeStatus, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    session.execute(update(pulse).values({"blocked": new_status.status}).where(pulse.c.id == pulseID))
    session.commit()
