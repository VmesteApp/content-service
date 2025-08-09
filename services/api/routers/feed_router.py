from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session

from services.api.role_checker import RoleChecker
from services.data.repositories.db_application_repository import DataBaseApplicationRepository

from src.domain.use_cases.application_use_case.get_user_application import GetUserApplications

from src.adapters.feed_adapter import FeedAdapter

from src.domain.dto.feed_dto.get_feed import GetFeedInputDto
from src.domain.dto.pulse_dto.get_pulse import GetPulseOutputDto


router = APIRouter()


@router.get("/application/my/")
def find_application(request: Request, session: Session = Depends(create_session),
                     role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBaseApplicationRepository(session)

    input_dto: GetFeedInputDto = FeedAdapter.request_to_get_user_applications_input_dto(user_id=request.state.id)

    use_case = GetUserApplications(repository)
    output_dto: List[GetPulseOutputDto] = use_case.execute(input_dto)

    response = FeedAdapter.get_user_applications_output_dto_to_responce(output_dto)

    return response
