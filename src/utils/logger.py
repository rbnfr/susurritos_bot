import logging
from functools import lru_cache


@lru_cache
def get_logger():
    """
    Configura y devuelve una instancia cacheada del logger
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)
