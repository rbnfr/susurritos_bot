from pydub import AudioSegment
from pathlib import Path


def get_audio_format(file_path: Path) -> str:
    """
    Determina el formato de un archivo de audio

    Args:
        file_path (Path): Ruta al archivo de audio

    Returns:
        str: Formato del audio (mp3, ogg, etc.)
    """
    return file_path.suffix.lower().lstrip('.')


def is_valid_audio(file_path: Path) -> bool:
    """
    Verifica si un archivo es un audio válido

    Args:
        file_path (Path): Ruta al archivo a verificar

    Returns:
        bool: True si es un archivo de audio válido
    """
    try:
        AudioSegment.from_file(file_path)
        return True
    except Exception:
        return False
