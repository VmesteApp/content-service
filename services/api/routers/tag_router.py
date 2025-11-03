from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session
from services.api.role_checker import RoleChecker
from services.data.repositories.db_tag_repository import DataBaseTagRepository

from src.domain.use_cases.tag_use_case.create_tag import CreateTag
from src.domain.use_cases.tag_use_case.update_tag import UpdateTag
from src.domain.use_cases.tag_use_case.delete_tag import DeleteTag
from src.domain.use_cases.tag_use_case.get_tags import GetTags

from src.adapters.tag_adapter import TagAdapter

from src.domain.dto.tag_dto.create_tag import CreateTagInputDto, CreateTagOutputDto
from src.domain.dto.tag_dto.update_tag import UpdateTagInputDto, UpdateTagOutputDto
from src.domain.dto.tag_dto.delete_tag import DeleteTagInputDto, DeleteTagOutputDto
from src.domain.dto.tag_dto.get_tags import GetTagsOutputDto

from services.api.schemas.tag_schemas import CreateTagSchema, UpdateTagSchema


router = APIRouter()


@router.post("/admin/tags")
async def create_tag(
    request: Request, 
    data: CreateTagSchema, 
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseTagRepository(session)

    input_dto: CreateTagInputDto = TagAdapter.request_to_create_tag_input_dto(data.model_dump())

    use_case = CreateTag(repository)
    output_dto: CreateTagOutputDto = use_case.execute(input_dto)

    response = TagAdapter.create_tag_output_dto_to_response(output_dto)

    return response


@router.put("/admin/tags")
async def update_tag(
    request: Request, 
    data: UpdateTagSchema, 
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseTagRepository(session)

    input_dto: UpdateTagInputDto = TagAdapter.request_to_update_tag_input_dto(data.model_dump())

    use_case = UpdateTag(repository)
    output_dto: UpdateTagOutputDto = use_case.execute(input_dto)

    response = TagAdapter.update_tag_output_dto_to_response(output_dto)

    return response


@router.delete("/admin/tags/{tag_id}")
async def delete_tag(
    request: Request, 
    tag_id: int, 
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseTagRepository(session)

    input_dto: DeleteTagInputDto = TagAdapter.request_to_delete_tag_input_dto(tag_id)

    use_case = DeleteTag(repository)
    output_dto: DeleteTagOutputDto = use_case.execute(input_dto)

    response = TagAdapter.delete_tag_output_dto_to_response(output_dto)

    return response


@router.get("/tags")
async def all_tags(session: Session = Depends(create_session)):
    repository = DataBaseTagRepository(session)

    input_dto = TagAdapter.request_to_get_tags_input_dto()

    use_case = GetTags(repository)
    output_dto: List[GetTagsOutputDto] = use_case.execute(input_dto)

    response = TagAdapter.get_tags_output_dto_to_response(output_dto)

    return {"tags": response}
