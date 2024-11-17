import vk_api
from app.config import vk_token

vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()