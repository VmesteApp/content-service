from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session

from services.api.schemas.application_schemas import SendApplication, Verdict
from services.api.role_checker import RoleChecker
from services.data.repositories.db_application_repository import DataBaseApplicationRepository

from src.domain.use_cases.application_use_case.create_application import CreateApplication
from src.domain.use_cases.pulse_use_case.update_pulse import UpdatePulse
from src.domain.use_cases.pulse_use_case.delete_pulse import DeletePulse
from src.domain.use_cases.pulse_use_case.get_pulses import GetPulses
from src.domain.use_cases.pulse_use_case.get_pulse import GetPulse

from src.adapters.application_adapter import ApplicationAdapter

from src.domain.dto.application_dto.create_application import CreatePulseInputDto, CreatePulseOutputDto
from src.domain.dto.application_dto.update_application import UpdateApplicationInputDto, UpdateApplicationOutputDto
from src.domain.dto.application_dto.get_user_applications import GetUserApplicationInputDto, GetUserApplicationOutputDto
from src.domain.dto.application_dto.get_pulse_applications import GetPulseApplicationInputDto, GetPulseApplicationOutputDto


router = APIRouter()


@router.post("/application")
async def create_application(request: Request, new_application: SendApplication, session: Session = Depends(create_session),
                             role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    pass


@router.put("/application/{id}/verdict")
async def update_application(request: Request, id: int, verdict: Verdict, session: Session = Depends(create_session),
                             role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    pass


@router.get("/application/{pulse_id}")
def find_application(pulse_id: int, request: Request, session: Session = Depends(create_session),
                     role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    pass


@router.get("/application/my/")
def find_application(request: Request, session: Session = Depends(create_session),
                     role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    pass
