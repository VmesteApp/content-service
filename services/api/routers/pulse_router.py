from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session

from services.api.schemas.pulse_schemas import CreatePulseSchemas, UpdatePulseSchemas
from services.api.role_checker import RoleChecker
from services.data.repositories.db_pulse_repository import DataBasePulseRepository

from src.domain.use_cases.pulse_use_case.create_pulse import CreatePulse
from src.domain.use_cases.pulse_use_case.update_pulse import UpdatePulse
from src.domain.use_cases.pulse_use_case.delete_pulse import DeletePulse
from src.domain.use_cases.pulse_use_case.get_pulses import GetPulses
from src.domain.use_cases.pulse_use_case.get_pulse import GetPulse

from src.adapters.pulse_adapter import PulseAdapter

from src.domain.dto.pulse_dto.create_pulse import CreatePulseInputDto, CreatePulseOutputDto
from src.domain.dto.pulse_dto.delete_pulse import DeletePulseInputDto, DeletePulseOutputDto
from src.domain.dto.pulse_dto.get_pulse import GetPulseInputDto, GetPulseOutputDto
from src.domain.dto.pulse_dto.update_pulse import UpdatePulseInputDto, UpdatePulseOutputDto


router = APIRouter()

ALLOWED_CATEGORIES = ["project", "event"]


@router.post("/pulse")
async def create_pulse(request: Request, data: CreatePulseSchemas, session: Session = Depends(create_session),
                       role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBasePulseRepository(session)

    input_dto: CreatePulseInputDto = PulseAdapter.request_to_create_pulse_input_dto(user_id=request.state.uid, create_pulse_input_dto=data.model_dump())

    use_case = CreatePulse(repository)
    output_dto: CreatePulseOutputDto = use_case.execute(input_dto)

    response = PulseAdapter.create_pulse_output_dto_to_responce(output_dto)

    return response


@router.put("/pulse")
async def update_pulse(request: Request, data: UpdatePulseSchemas, session: Session = Depends(create_session),
                       role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    
    repository = DataBasePulseRepository(session)

    input_dto: UpdatePulseInputDto = PulseAdapter.request_to_update_pulse_input_dto(update_pulse_input_dto=data.model_dump())

    use_case = UpdatePulse(repository)
    output_dto: UpdatePulseOutputDto = use_case.execute(input_dto)

    response = PulseAdapter.update_pulse_output_dto_to_responce(output_dto)

    return response


@router.delete("/pulse/{delete_pulse}")
def delete_pulse(request: Request, delete_pulse: int, session: Session = Depends(create_session),
                 role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)

    repository = DataBasePulseRepository(session)

    input_dto: DeletePulseInputDto = PulseAdapter.request_to_delete_pulse_input_dto(pulse_id=delete_pulse)

    use_case = DeletePulse(repository)
    output_dto: DeletePulseOutputDto = use_case.execute(input_dto)

    response = PulseAdapter.delete_pulse_output_dto_to_responce(output_dto)

    return response


@router.get("/pulses/my/")
def all_pulses(request: Request, session: Session = Depends(create_session)):
    repository = DataBasePulseRepository(session)

    input_dto: GetPulseInputDto = PulseAdapter.request_to_get_pulses_input_dto(user_id=request.state.uid)
    
    use_case = GetPulses(repository)
    output_dto: List[GetPulseOutputDto] = use_case.execute(input_dto)

    response = PulseAdapter.get_pulses_output_dto_to_responce(output_dto)

    return response


@router.get("/pulses/{pulse_id}")
def find_pulse(pulse_id: int, session: Session = Depends(create_session)):
    repository = DataBasePulseRepository(session)

    input_dto: GetPulseInputDto = PulseAdapter.request_to_get_pulse_input_dto(pulse_id=pulse_id)

    use_case = GetPulse(repository)
    output_dto: GetPulseOutputDto = use_case.execute(input_dto)
    print(output_dto)
    response = PulseAdapter.get_pulse_output_dto_to_responce(output_dto)

    return response
