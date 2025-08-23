from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session
from services.api.role_checker import RoleChecker
from services.data.repositories.db_feed_repository import DataBaseFeedRepository

from src.domain.use_cases.feed_use_case.get_feed import GetFeed
from src.adapters.feed_adapter import FeedAdapter
from src.domain.dto.feed_dto.get_feed import GetFeedInputDto, GetFeedOutputDto


router = APIRouter()


@router.get("/feed")
def get_feed(
    request: Request,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    tags: Optional[List[int]] = Query(None),
    name: Optional[str] = None,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["user"])
    ):
    role_checker(request)

    repository = DataBaseFeedRepository(session)

    input_dto: GetFeedInputDto = FeedAdapter.request_to_get_feed_input_dto(
        user_id=request.state.uid,
        skip=skip,
        limit=limit,
        tags=tags,
        name=name
    )

    use_case = GetFeed(repository)
    output_dto: List[GetFeedOutputDto] = use_case.execute(input_dto)

    response = FeedAdapter.get_feed_output_dto_to_response(output_dto)

    return response
