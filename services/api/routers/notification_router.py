from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session
from services.api.role_checker import RoleChecker
from services.data.repositories.db_notification_repository import DataBaseNotificationRepository

from src.domain.use_cases.notification_use_case.get_notifications import GetNotifications
from src.domain.use_cases.notification_use_case.create_notification import CreateNotification

from src.adapters.notification_adapter import NotificationAdapter

from src.domain.dto.notification_dto.get_notifications import GetNotificationsInputDto, GetNotificationsOutputDto
from src.domain.dto.notification_dto.create_notification import CreateNotificationInputDto, CreateNotificationOutputDto

from services.api.schemas.notification_schemas import NotificationListResponseSchema, CreateNotificationSchema


router = APIRouter()


@router.get("/notifications/my", response_model=NotificationListResponseSchema)
def all_notifications(
    request: Request, 
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["user"])
):
    role_checker(request)

    repository = DataBaseNotificationRepository(session)

    input_dto: GetNotificationsInputDto = NotificationAdapter.request_to_get_notifications_input_dto(
        user_id=request.state.uid
    )

    use_case = GetNotifications(repository)
    output_dto: List[GetNotificationsOutputDto] = use_case.execute(input_dto)

    response = NotificationAdapter.get_notifications_output_dto_to_response(output_dto)

    return response


@router.post("/notifications")
async def create_notification(
    request: Request, 
    data: CreateNotificationSchema,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseNotificationRepository(session)

    input_dto: CreateNotificationInputDto = NotificationAdapter.request_to_create_notification_input_dto(
        user_id=data.user_id,
        text=data.text
    )

    use_case = CreateNotification(repository)
    output_dto: CreateNotificationOutputDto = use_case.execute(input_dto)

    response = NotificationAdapter.create_notification_output_dto_to_response(output_dto)

    return response
