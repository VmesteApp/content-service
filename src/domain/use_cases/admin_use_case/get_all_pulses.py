from typing import List
from src.domain.dto.admin_dto.get_all_pulses import GetAllPulsesInputDto, GetAllPulsesOutputDto
from src.domain.interfaces.admin_repository import AdminRepository


class GetAllPulses:
    def __init__(self, repository: AdminRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetAllPulsesInputDto) -> List[GetAllPulsesOutputDto]:
        try:
            return self.repository.get_all_pulses(dto.skip, dto.limit)
        except Exception as error:
            raise Exception(f"Failed to get pulses: {str(error)}")
