# from services.vk_session import vk
# from src.domain.interfaces.external.vk_service import VkService


# class VkServiceImpl(VkService):
#     def send_notification(self, user_ids: list, message: str, title: str, button: str) -> bool:
#         try:
#             response = vk.notifications.sendMessage(
#                 user_ids=user_ids,
#                 message=message,
#                 title=title,
#                 button=button
#             )
#             return True
#         except Exception as e:
#             print(f"VK API error: {e}")
#             return False
