from fastapi import APIRouter, Request, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.models import notification
from app.api.role_checker import RoleChecker

router = APIRouter()

@router.get("/notifications")
def all_notifications(request: Request, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["admin", "superadmin"])):
    role_checker(request)
    all_notif = session.query(notification)
    return {"complaints": [{"id": i.id,
                    "user_id" : i.user_id,
                    "text": i.text,
                    } for i in all_notif]}