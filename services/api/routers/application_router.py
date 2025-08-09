from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session

from services.api.schemas.application_schemas import SendApplication, Verdict
from services.api.role_checker import RoleChecker
from services.data.repositories.db_application_repository import DataBaseApplicationRepository

from src.domain.use_cases.application_use_case.create_application import CreateApplication
from src.domain.use_cases.application_use_case.update_application import UpdateApplication
from src.domain.use_cases.application_use_case.get_pulse_application import GetPulseApplications
from src.domain.use_cases.application_use_case.get_user_application import GetUserApplications

from src.adapters.application_adapter import ApplicationAdapter

from src.domain.dto.application_dto.create_application import CreateApplicationInputDto, CreateApplicationOutputDto
from src.domain.dto.application_dto.update_application import UpdateApplicationInputDto, UpdateApplicationOutputDto
from src.domain.dto.application_dto.get_user_applications import GetUserApplicationsInputDto, GetUserApplicationsOutputDto
from src.domain.dto.application_dto.get_pulse_applications import GetPulseApplicationsInputDto, GetPulseApplicationsOutputDto


router = APIRouter()


@router.post("/application")
async def create_application(request: Request, data: SendApplication, session: Session = Depends(create_session),
                             role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBaseApplicationRepository(session)

    input_dto: CreateApplicationInputDto = ApplicationAdapter.request_to_create_application_input_dto(create_application_input_dto=data.model_dump())

    use_case = CreateApplication(repository)
    output_dto: CreateApplicationOutputDto = use_case.execute(input_dto)

    response = ApplicationAdapter.create_applications_output_dto_to_responce(output_dto)

    return response


@router.put("/application/{id}/verdict")
async def update_application(request: Request, id: int, data: Verdict, session: Session = Depends(create_session),
                             role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBaseApplicationRepository(session)

    input_dto: UpdateApplicationInputDto = ApplicationAdapter.request_to_update_application_input_dto(application_id=id, update_application_input_dto=data.model_dump())

    use_case = UpdateApplication(repository)
    output_dto: UpdateApplicationOutputDto = use_case.execute(input_dto)

    response = ApplicationAdapter.update_application_output_dto_to_responce(output_dto)

    return response


@router.get("/application/{pulse_id}")
def find_application(pulse_id: int, request: Request, session: Session = Depends(create_session),
                     role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBaseApplicationRepository(session)

    input_dto: GetPulseApplicationsInputDto = ApplicationAdapter.request_to_get_pulse_applications_input_dto(pulse_id=pulse_id)

    use_case = GetPulseApplications(repository)
    output_dto: List[GetPulseApplicationsOutputDto] = use_case.execute(input_dto)

    response = ApplicationAdapter.get_pulse_applications_dto_to_responce(output_dto)

    return response


@router.get("/application/my/")
def find_application(request: Request, session: Session = Depends(create_session),
                     role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBaseApplicationRepository(session)

    input_dto: GetUserApplicationsInputDto = ApplicationAdapter.request_to_get_user_applications_input_dto(user_id=request.state.id)

    use_case = GetUserApplications(repository)
    output_dto: List[GetUserApplicationsOutputDto] = use_case.execute(input_dto)

    response = ApplicationAdapter.get_user_applications_output_dto_to_responce(output_dto)

    return response
