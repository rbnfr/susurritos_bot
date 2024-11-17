from pathlib import Path
import uuid
import os
from utils.logger import get_logger

logger = get_logger()


def generate_temp_filename(original_path: str) -> str:
    """
    Genera un nombre de archivo temporal único

    Args:
        original_path (str): Ruta original del archivo

    Returns:
        str: Nombre de archivo único
    """
    extension = Path(original_path).suffix
    return f"{uuid.uuid4()}{extension}.oga"


def cleanup_file(file_path: Path) -> None:
    """
    Elimina un archivo temporal

    Args:
        file_path (Path): Ruta al archivo a eliminar
    """
    try:
        if file_path.exists():
            os.remove(file_path)
    except Exception as e:
        # Solo loggeamos el error pero no lo propagamos
        # ya que este es un proceso de limpieza secundario
        logger.error(f"Error al eliminar archivo temporal {file_path}: {str(e)}")
