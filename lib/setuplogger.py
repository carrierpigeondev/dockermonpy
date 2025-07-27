
import logging
from logging.handlers import RotatingFileHandler

import pathlib

LEVEL = logging.INFO

CONFIG_PATH = pathlib.Path.home() / ".config" / "dockermonpy"
LOG_FILE    = CONFIG_PATH / "log.log"

def make_logger():
    logger = logging.getLogger("dockermonpy")
    logger.setLevel(LEVEL)
    if logger.hasHandlers():
        logger.handlers.clear()
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LEVEL)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger