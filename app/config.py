from dotenv import load_dotenv
import os


load_dotenv()

DB_URL = os.environ.get("DB_URL")
SECRET = os.environ.get("SECRET")
MODEL_PATH = os.environ.get("MODEL_PATH")
VOCAB_PATH = os.environ.get("VOCAB_PATH")
MODERATION_ON = os.environ.get("MODERATION_ON") == "True"
vk_token = os.environ.get("vk_token")
