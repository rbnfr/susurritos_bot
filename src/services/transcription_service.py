import whisperx
from pathlib import Path
from config.config import get_settings
from utils.logger import get_logger

settings = get_settings()
logger = get_logger()


# Cargar el modelo al iniciar (singleton)
try:
    asr_options = {
        "hotwords": None,
    }
    model = whisperx.load_model(
        whisper_arch=settings.whisperx_model_size,
        device=settings.whisperx_device,
        compute_type=settings.whisperx_compute_type,
        asr_options=asr_options,
    )
except Exception as e:
    logger.error(f"Error al cargar el modelo de Whisper: {str(e)}")
    raise


def transcribe_audio(audio_path: Path) -> str:
    """
    Transcribe un archivo de audio usando el modelo Whisper

    Args:
        audio_path (Path): Ruta al archivo de audio WAV

    Returns:
        str: Texto transcrito
    """
    try:
        # Realizar la transcripción
        result = model.transcribe(str(audio_path))

        # Diccionario con los segmentos de la transcripción
        segments = result['segments']

        # Unir todos los segmentos en un solo texto
        transcription = ' '.join([segment['text'] for segment in segments])

        return transcription.strip()

    except Exception as e:
        logger.error(f"Error al transcribir el audio: {str(e)}")
        raise
