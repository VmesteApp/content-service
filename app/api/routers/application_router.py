from fastapi import APIRouter, HTTPException, Depends
from app.api.jwt_decoder import current_user
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, select
from app.models.models import application
from app.schemas.applications_schemas import Send_Application, Verdict


router = APIRouter()


@router.post("/application")
async def create_application(session: Session = Depends(get_db), new_application: Send_Application = Depends()):
    if current_user["role"] == "user":
        post_application = insert(application).values(**new_application.dict())
        session.execute(post_application)
        session.commit()  
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")        

    
@router.post("/application/verdict")
async def update_appli(session: Session = Depends(get_db), verdict: Verdict = Depends()):
    if current_user["role"] == "user":
        appli = update(application)
        val = appli.values({"status": verdict.status})
        cond = val.where(application.c.id == verdict.id)
        res = session.execute(cond)
        session.commit()  
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")
    

    

@router.get("/application/{pulse_id}")
def find_application(pulse_id_new: int, session: Session = Depends(get_db)):
    if current_user["role"] == "user":
        result = session.execute(select(application).where(application.c.pulse_id == pulse_id_new))
        return {
                "status": "success",
                "data": result.scalars().all(),
                "details": None
            }
    else:
        raise HTTPException(status_code=403, detail=" Invalid role type")
