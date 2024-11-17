import asyncio
import sys
from telethon import TelegramClient
from telethon import events
from services.audio_service import download_audio, convert_to_wav
from services.transcription_service import transcribe_audio
from utils.file_utils import cleanup_file
from utils.logger import get_logger
from config.config import get_settings

settings = get_settings()
logger = get_logger()

active_chats = set()


def register_handlers(client: TelegramClient):
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        if not event.is_private:
            return

        active_chats.add(event.chat_id)

        username = await client.get_entity(event.sender_id)

        await event.reply(
            f"Hello {username.first_name}! I'm a bot that transcribes audio to text.\n\n"
            "📝 **Available commands:**\n"
            "/start - Shows this help message\n"
            "/help - Shows this help message\n"
            "/shutdown - Shuts down the bot (only for admins)\n\n"
            "🎵 **Usage:**\n"
            "1. Send me a voice message\n"
            "2. Send me an audio file\n"
            "3. Re-send me a voice message from another chat or another app\n\n"
            "I will transcribe the audio to text and send it back to you as a response."
        )

    @client.on(events.NewMessage(pattern='/stop'))
    async def stop_handler(event):
        if not event.is_private:
            return
        active_chats.discard(event.chat_id)
        await event.reply("Bot stopped. Use /start to activate again.")

    @client.on(events.NewMessage(pattern='/help'))
    async def help_handler(event):
        if not event.is_private:
            return
        await start_handler(event)

    @client.on(events.NewMessage)
    async def message_handler(event):
        try:
            if event.chat_id not in active_chats:
                return

            if not _is_valid_message(event):
                return

            processing_message = await event.reply("Processing audio...")
            transcription = await _process_audio(event.message)
            username = await client.get_entity(event.sender_id)
            user_id = await client.get_me()

            await event.reply("📝 Transcription:\n\n" + transcription)
            await processing_message.delete()

            logger.info(f"Transcription sent to user {username.first_name} ({user_id.id})")
        except Exception as e:
            logger.error(f"Error al procesar el audio: {str(e)}")
            await event.reply("❌ Sorry, there was an error processing the audio. Please try again.")

    def _is_valid_message(event):
        if not event.is_private or not event.message.media:
            return False

        is_voice = event.message.voice
        is_audio = event.message.audio
        is_audio_document = (
            hasattr(event.message.media, 'document') and
            event.message.media.document.mime_type and
            event.message.media.document.mime_type.startswith('audio/')
        )

        return is_voice or is_audio or is_audio_document

    async def _process_audio(message):
        audio_path = await download_audio(message)
        wav_path = convert_to_wav(audio_path)
        transcription = transcribe_audio(wav_path)

        cleanup_file(audio_path)
        if audio_path != wav_path:
            cleanup_file(wav_path)

        return transcription

    @client.on(events.NewMessage(pattern='/shutdown'))
    async def shutdown_handler(event):
        try:
            if event.sender_id not in settings.admin_users:
                await event.reply("❌ You don't have permission to shut down the bot 🖕.")
                return

            logger.info(f"Shutdown command received from user {event.sender_id}")

            await event.reply("🔄 Shutting down the bot...")

            await asyncio.sleep(1)

            await client.disconnect()

            sys.exit(0)

        except Exception as e:
            logger.error(f"Error when shutting down the bot: {str(e)}")
            await event.reply("❌ You cannot shut down the bot 🖕.")
