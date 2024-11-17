from telethon.sync import TelegramClient
from telethon.tl.types import BotCommand, BotCommandScopeDefault
from telethon.tl.functions.bots import SetBotCommandsRequest
from config.config import get_settings
from utils.logger import get_logger

settings = get_settings()
logger = get_logger()


async def setup_bot_commands(client: TelegramClient):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
    ]

    if settings.admin_users:
        commands.append(BotCommand(command="shutdown", description="Shuts down the bot (only for admins)"))

    try:
        await client(SetBotCommandsRequest(commands, BotCommandScopeDefault()))
    except Exception as e:
        logger.error(f"Error setting up bot commands: {e}")
