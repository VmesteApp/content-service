from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.complaint import Complaint
from src.domain.dto.complaint_dto.get_complaints import GetComplaintsOutputDto


class ComplaintRepository(ABC):
    @abstractmethod
    def create_complaint(self, complaint: Complaint) -> bool:
        pass

    @abstractmethod
    def get_all_complaints(self) -> List[GetComplaintsOutputDto]:
        pass

    @abstractmethod
    def update_complaint_status(self, complaint_id: int, status: str) -> bool:
        pass

    @abstractmethod
    def get_complaint_details(self, complaint_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def block_pulse(self, pulse_id: int) -> bool:
        pass

    @abstractmethod
    def create_notification(self, user_id: int, text: str) -> bool:
        pass
