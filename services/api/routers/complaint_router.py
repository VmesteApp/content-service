from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session
from services.api.role_checker import RoleChecker
from services.data.repositories.db_complaint_repository import DataBaseComplaintRepository
from services.data.external.vk_service_impl import VkServiceImpl
from services.data.external.grpc_service_impl import GrpcServiceImpl

from src.domain.use_cases.complaint_use_case.create_complaint import CreateComplaint
from src.domain.use_cases.complaint_use_case.get_complaints import GetComplaints
from src.domain.use_cases.complaint_use_case.update_complaint import UpdateComplaint

from src.adapters.complaint_adapter import ComplaintAdapter

from src.domain.dto.complaint_dto.create_complaint import CreateComplaintInputDto, CreateComplaintOutputDto
from src.domain.dto.complaint_dto.get_complaints import GetComplaintsOutputDto
from src.domain.dto.complaint_dto.update_complaint import UpdateComplaintInputDto, UpdateComplaintOutputDto

from services.api.schemas.complaint_schemas import CreateComplaintSchema, VerdictComplaintSchema


router = APIRouter()


@router.post("/pulses/{pulse_id}/complaint")
def create_complaint(
    request: Request, 
    pulse_id: int, 
    data: CreateComplaintSchema,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["user"])
):
    role_checker(request)

    repository = DataBaseComplaintRepository(session)

    input_dto: CreateComplaintInputDto = ComplaintAdapter.request_to_create_complaint_input_dto(
        pulse_id=pulse_id, 
        data=data.model_dump()
    )

    use_case = CreateComplaint(repository)
    output_dto: CreateComplaintOutputDto = use_case.execute(input_dto)

    response = ComplaintAdapter.create_complaint_output_dto_to_response(output_dto)

    return response


@router.get("/complaints")
def all_complaints(
    request: Request, 
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseComplaintRepository(session)

    input_dto = ComplaintAdapter.request_to_get_complaints_input_dto()

    use_case = GetComplaints(repository)
    output_dto: List[GetComplaintsOutputDto] = use_case.execute(input_dto)

    response = ComplaintAdapter.get_complaints_output_dto_to_response(output_dto)

    return response


@router.put("/complaints/{complaint_id}/verdict")
async def update_complaint(
    request: Request, 
    complaint_id: int, 
    data: VerdictComplaintSchema,
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["admin", "superadmin"])
):
    role_checker(request)

    repository = DataBaseComplaintRepository(session)
    vk_service = VkServiceImpl()
    grpc_service = GrpcServiceImpl()

    input_dto: UpdateComplaintInputDto = ComplaintAdapter.request_to_update_complaint_input_dto(
        complaint_id=complaint_id, 
        data=data.model_dump()
    )

    use_case = UpdateComplaint(repository, vk_service, grpc_service)
    output_dto: UpdateComplaintOutputDto = use_case.execute(input_dto)

    response = ComplaintAdapter.update_complaint_output_dto_to_response(output_dto)

    return response
