from bot.bot_instance import get_client
from bot.handlers import register_handlers
from bot.commands import setup_bot_commands
from config.config import get_settings
from utils.logger import get_logger

settings = get_settings()
logger = get_logger()


async def main():
    try:
        client = get_client()

        await setup_bot_commands(client)
        register_handlers(client)

        logger.info("Bot started. Waiting for messages...")
        logger.info("Available commands:")
        logger.info("/shutdown - Shuts down the bot (only for admins)")

        try:
            await client.start(bot_token=settings.telegram_bot_token)
            await client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("Bot stopped by keyboard interrupt")
        finally:
            await client.disconnect()

    except Exception as e:
        logger.error(f"Error al iniciar el bot: {str(e)}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
