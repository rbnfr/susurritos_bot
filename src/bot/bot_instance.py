from telethon.sync import TelegramClient
from telethon.sessions import MemorySession
from config.config import get_settings
from utils.logger import get_logger
from functools import lru_cache

settings = get_settings()
logger = get_logger()


@lru_cache()
def get_client() -> TelegramClient:

    return TelegramClient(
        MemorySession(),
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash
    )
