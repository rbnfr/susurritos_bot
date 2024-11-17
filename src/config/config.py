from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    telegram_bot_token: str = Field(..., description="Telegram bot token")
    telegram_api_id: str = Field(..., description="Telegram API ID")
    telegram_api_hash: str = Field(..., description="Telegram API hash")

    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    downloads_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "downloads")
    session_name: str = "bot_session"

    whisperx_model_size: str = "medium"
    whisperx_device: str = "cuda"
    whisperx_compute_type: str = "float16"

    admin_users: list[int] = []

    def model_post_init(self, *args, **kwargs):
        self.downloads_dir.mkdir(parents=True, exist_ok=True)

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
