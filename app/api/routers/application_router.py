from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, select
from app.models.models import application
from app.schemas.applications_schemas import Send_Application, Verdict


router = APIRouter()


@router.post("content/application")
async def create_application(request: Request, new_application: Send_Application,  session: Session = Depends(get_db)):
    if request.state.role == "user":
        post_application = insert(application).values(**new_application.dict())
        session.execute(post_application)
        session.commit()  
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")        


@router.post("content/application/verdict")
async def update_appli(request: Request, verdict: Verdict, session: Session = Depends(get_db)):
    if request.state.role == "user":
        appli = update(application)
        val = appli.values({"status": verdict.status})
        cond = val.where(application.c.id == verdict.id)
        res = session.execute(cond)
        session.commit()
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")


@router.get("content/application/{pulse_id}")
def find_application(pulse_id: int, request: Request, session: Session = Depends(get_db)):
    if request.state.role == "user":
        result = session.execute(select(application).where(application.c.pulse_id == pulse_id))
        return {
                "status": "success",
                "data": result.scalars().all(),
                "details": None
            }
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")
