from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete
from app.models.models import tag
from app.schemas.tag_schemas import Create_Tag, Update_Tag, Delete_Tag


router = APIRouter()


@router.post("/admin/tags")
async def create_tag(request: Request, new_tag: Create_Tag, session: Session = Depends(get_db)):
    if request.state.role == "admin" or request.state.role == "super_admin":
        post_tag = insert(tag).values({"name": new_tag.name})
        session.execute(post_tag)
        session.commit()
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")


@router.put("/admin/tags")
async def update_tag(request: Request, up_tag: Update_Tag, session: Session = Depends(get_db)):
    if request.state.role == "admin":
        update_tag = update(tag)
        val = update_tag.values({"name": up_tag.name})
        cond = val.where(tag.c.id == up_tag.id)
        session.execute(cond)
        session.commit()  
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type") 


@router.delete("/admin/tags")
async def delete_tag(request: Request, del_tag: Delete_Tag, session: Session = Depends(get_db)):
    if request.state.role == "admin":
        result = session.execute(delete(tag).where(del_tag.id == tag.c.id))
        session.commit()  
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")
    

@router.get("/tags")
def all_pulse(session: Session = Depends(get_db)):
    tags = session.query((tag)).all()
    return {"pulses": [list(tag_1) for tag_1 in tags]}