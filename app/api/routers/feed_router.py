from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.models import pulse, images


router = APIRouter()


@router.get("/feed")
def get_feed(session: Session = Depends(get_db)):
    result = session.query(pulse).all()
    return [{"id": res.id,
            "category": res.category,
            "name": res.name,
            "founder_id": res.founder_id,
            "description": res.description,
            "short_description": res.short_description,
            "images": [j[3] for j in session.query(images).where(images.c.pulse_id == res.id).all()]
            } for res in result]
