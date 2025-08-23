from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session
from services.api.role_checker import RoleChecker
from services.data.repositories.db_admin_repository import DataBaseAdminRepository

from src.domain.use_cases.admin_use_case.change_status import ChangeStatus
from src.domain.use_cases.admin_use_case.get_all_pulses import GetAllPulses
from src.domain.use_cases.admin_use_case.create_pulse_admin import CreatePulseAdmin
from src.domain.use_cases.admin_use_case.update_pulse_admin import UpdatePulseAdmin

from src.adapters.admin_adapter import AdminAdapter

from src.domain.dto.admin_dto.change_status import ChangeStatusInputDto, ChangeStatusOutputDto
from src.domain.dto.admin_dto.get_all_pulses import GetAllPulsesOutputDto
from src.domain.dto.admin_dto.create_pulse_admin import CreatePulseAdminInputDto, CreatePulseAdminOutputDto
from src.domain.dto.admin_dto.update_pulse_admin import UpdatePulseAdminInputDto, UpdatePulseAdminOutputDto

from services.api.schemas.admin_schemas import ChangeStatusSchema, CreatePulseAdminSchema, UpdatePulseAdminSchema


router = APIRouter()


@router.put("/admin/pulse/{pulse_id}/moderation")
def change_status(
    request: Request, 
    pulse_id: int, 
    data: ChangeStatusSchema,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseAdminRepository(session)

    input_dto: ChangeStatusInputDto = AdminAdapter.request_to_change_status_input_dto(
        pulse_id=pulse_id, 
        blocked=data.blocked
    )

    use_case = ChangeStatus(repository)
    output_dto: ChangeStatusOutputDto = use_case.execute(input_dto)

    response = AdminAdapter.change_status_output_dto_to_response(output_dto)

    return response


@router.get("/admin/pulses")
def all_pulses_admin(
    request: Request,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseAdminRepository(session)

    input_dto = AdminAdapter.request_to_get_all_pulses_input_dto(skip=skip, limit=limit)

    use_case = GetAllPulses(repository)
    output_dto: List[GetAllPulsesOutputDto] = use_case.execute(input_dto)

    response = AdminAdapter.get_all_pulses_output_dto_to_response(output_dto)

    return response


@router.post("/admin/pulse")
async def create_pulse_admin(
    request: Request, 
    data: CreatePulseAdminSchema,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseAdminRepository(session)

    input_dto: CreatePulseAdminInputDto = AdminAdapter.request_to_create_pulse_admin_input_dto(data.model_dump())

    use_case = CreatePulseAdmin(repository)
    output_dto: CreatePulseAdminOutputDto = use_case.execute(input_dto)

    response = AdminAdapter.create_pulse_admin_output_dto_to_response(output_dto)

    return response


@router.put("/admin/pulse")
async def update_pulse_admin(
    request: Request, 
    data: UpdatePulseAdminSchema,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseAdminRepository(session)

    input_dto: UpdatePulseAdminInputDto = AdminAdapter.request_to_update_pulse_admin_input_dto(data.model_dump())

    use_case = UpdatePulseAdmin(repository)
    output_dto: UpdatePulseAdminOutputDto = use_case.execute(input_dto)

    response = AdminAdapter.update_pulse_admin_output_dto_to_response(output_dto)

    return response
