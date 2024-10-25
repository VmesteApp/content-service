from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete
from app.models.models import tag
from app.schemas.tag_schemas import CreateTag, UpdateTag, DeleteTag
from app.api.role_checker import RoleChecker


router = APIRouter()


@router.post("/admin/tags")
async def create_tag(request: Request, new_tag: CreateTag, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    post_tag = insert(tag).values({"name": new_tag.name})
    session.execute(post_tag)
    session.commit()



@router.put("/admin/tags")
async def update_tag(request: Request, up_tag: UpdateTag, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    update_tag = update(tag)
    val = update_tag.values({"name": up_tag.name})
    cond = val.where(tag.c.id == up_tag.id)
    session.execute(cond)
    session.commit()



@router.delete("/admin/tags")
async def delete_tag(request: Request, del_tag: DeleteTag, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    result = session.execute(delete(tag).where(del_tag.id == tag.c.id))
    session.commit()



@router.get("/tags")
def all_tags(session: Session = Depends(get_db)):
    tags = session.query((tag)).all()
    return {"tags": [{"id": i.id, "name": i.name} for i in tags]}
