import logging
from os import getcwd, path

from mtime import get_current_timestamp, convert_to_time


class GlobalLogger(logging.Logger):
    def error(self, msg, *args, **kwargs):
        super().error(msg, *args, **kwargs)
        exit(0)


def setup_logger():
    current_timestamp = get_current_timestamp()
    current_file_time = convert_to_time(current_timestamp)
    logger = GlobalLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
    )
    logger_file_path_all = path.join(getcwd(), "log", current_file_time + ".log")
    file_handler = logging.FileHandler(logger_file_path_all)
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


global_logger = setup_logger()
