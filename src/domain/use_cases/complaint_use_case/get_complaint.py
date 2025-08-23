from typing import List
from src.domain.dto.complaint_dto.get_complaints import GetComplaintsInputDto, GetComplaintsOutputDto
from src.domain.interfaces.complaint_repository import ComplaintRepository


class GetComplaints:
    def __init__(self, repository: ComplaintRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetComplaintsInputDto) -> List[GetComplaintsOutputDto]:
        try:
            return self.repository.get_all_complaints()
        except Exception as error:
            raise Exception(f"Failed to get complaints: {str(error)}")
