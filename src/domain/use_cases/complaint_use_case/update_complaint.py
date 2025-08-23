from src.domain.dto.complaint_dto.update_complaint import UpdateComplaintInputDto, UpdateComplaintOutputDto
from src.domain.interfaces.complaint_repository import ComplaintRepository
from src.domain.interfaces.external.vk_service import VkService
from src.domain.interfaces.external.grpc_service import GrpcService


class UpdateComplaint:
    def __init__(
        self, 
        repository: ComplaintRepository,
        vk_service: VkService,
        grpc_service: GrpcService
    ) -> None:
        self.repository = repository
        self.vk_service = vk_service
        self.grpc_service = grpc_service

    def execute(self, dto: UpdateComplaintInputDto) -> UpdateComplaintOutputDto:
        try:
            if dto.verdict == "APPROVED":
                complaint_details = self.repository.get_complaint_details(dto.complaint_id)
                if not complaint_details:
                    return UpdateComplaintOutputDto(
                        is_success=False,
                        error_message="Complaint not found"
                    )

                pulse_id = complaint_details["pulse_id"]

                user_id = self.repository.get_pulse_founder_id(pulse_id)
                pulse_name = self.repository.get_pulse_name(pulse_id)

                if not user_id:
                    return UpdateComplaintOutputDto(
                        is_success=False,
                        error_message="Pulse founder not found"
                    )

                self.repository.update_complaint_status(dto.complaint_id, "APPROVED")
                self.repository.block_pulse(pulse_id)

                vk_id = self.grpc_service.get_vk_id(user_id)

                if vk_id:
                    message = f"Ваш импульс '{pulse_name}' был заблокирован по жалобе"
                    self.vk_service.send_notification(
                        user_ids=[vk_id],
                        message=message,
                        title='Новое уведомление',
                        button='Перейти в приложение'
                    )

                self.repository.create_notification(user_id, message)

            else:
                self.repository.update_complaint_status(dto.complaint_id, "REJECTED")

            self.repository.session.commit()

            return UpdateComplaintOutputDto(
                is_success=True,
                error_message=""
            )

        except Exception as error:
            self.repository.session.rollback()
            return UpdateComplaintOutputDto(
                is_success=False,
                error_message=str(error)
            )
