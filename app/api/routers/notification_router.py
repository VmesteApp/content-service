from fastapi import APIRouter, Request, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.models import notification
from app.api.role_checker import RoleChecker

router = APIRouter()

@router.get("/notifications/my")
def all_notifications(request: Request, session: Session = Depends(get_db), role_checker = RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    all_notif = session.query(notification).where(notification.c.user_id == request.state.uid)
    return {"notifications": [{"id": i.id,
                    "user_id" : i.user_id,
                    "text": i.text,
                    "created_at": i.created_at,
                    } for i in all_notif]}
