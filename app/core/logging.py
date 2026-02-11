import logging
import sys

from pythonjsonlogger import jsonlogger

from app.core.config import settings


def setup_logging() -> None:
    log_level = logging.DEBUG if settings.debug else logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    # Évite les handlers dupliqués
    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.addHandler(handler)
