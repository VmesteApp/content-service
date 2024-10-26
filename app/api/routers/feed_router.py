from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.models import pulse, images, pulse_tags, tag


router = APIRouter()


@router.get("/feed")
def get_feed(session: Session = Depends(get_db)):
    result = session.query(pulse).join(pulse_tags, pulse_tags.c.pulse_id == pulse.c.id).all()
    tags = session.query(pulse_tags.c.pulse_id, tag.c.name, tag.c.id).join(tag, tag.c.id == pulse_tags.c.tag_id).all()
    return [{"id": res.id,
            "category": res.category,
            "name": res.name,
            "founder_id": res.founder_id,
            "description": res.description,
            "short_description": res.short_description,
            "images": [j[3] for j in session.query(images).where(images.c.pulse_id == res.id).all()],
            "tags": [[j[1], j[2]] for j in tags if j.pulse_id == res.id]
            } for res in result]
