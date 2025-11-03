from src.domain.dto.complaint_dto.create_complaint import CreateComplaintInputDto, CreateComplaintOutputDto
from src.domain.entities.complaint import Complaint
from src.domain.interfaces.complaint_repository import ComplaintRepository


class CreateComplaint:
    def __init__(self, repository: ComplaintRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: CreateComplaintInputDto) -> CreateComplaintOutputDto:
        try:
            complaint = Complaint(
                id=None,
                pulse_id=dto.pulse_id,
                message=dto.message
            )
            
            success = self.repository.create_complaint(complaint)
            
            return CreateComplaintOutputDto(
                is_success=success,
                error_message=""
            )
            
        except Exception as error:
            return CreateComplaintOutputDto(
                is_success=False,
                error_message=str(error)
            )
