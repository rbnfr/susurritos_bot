from pathlib import Path
from pydub import AudioSegment
from config.config import get_settings
from utils.file_utils import generate_temp_filename
from utils.logger import get_logger
from bot.bot_instance import get_client


settings = get_settings()
logger = get_logger()
client = get_client()


async def download_audio(message) -> Path:
    """
    Descarga un archivo de audio enviado a través de Telethon

    Args:
        media: Objeto media de Telethon

    Returns:
        Path: Ruta al archivo descargado
    """
    try:
        # Generar nombre de archivo temporal
        temp_filename = generate_temp_filename("audio")
        downloaded_file = settings.downloads_dir / temp_filename

        # Descargar el archivo
        await message.download_media(file=downloaded_file)

        return downloaded_file

    except Exception as e:
        logger.error(f"Error al descargar el audio: {str(e)}")
        raise


def convert_to_wav(audio_path: Path) -> Path:
    """
    Convierte un archivo de audio a formato WAV si es necesario

    Args:
        audio_path (Path): Ruta al archivo de audio original

    Returns:
        Path: Ruta al archivo WAV
    """
    try:
        if audio_path.suffix.lower() == '.wav':
            return audio_path

        # Cargar el audio con pydub
        audio = AudioSegment.from_file(audio_path)

        # Generar nombre para el archivo WAV
        wav_path = settings.downloads_dir / f"{audio_path.stem}.wav"

        # Exportar como WAV
        audio.export(wav_path, format='wav')

        return wav_path

    except Exception as e:
        logger.error(f"Error al convertir el audio a WAV: {str(e)}")
        raise
