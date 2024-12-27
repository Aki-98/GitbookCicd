from mstr import ENCODE
from logging import Logger

import logging
from colorama import init, Fore, Style

from mtime import get_current_timestamp, convert_to_time


class ErrorInLogger(Exception):
    def __init__(self, message):
        self.message = message


class GlobalLogger(logging.Logger):
    def error(self, msg, *args, **kwargs):
        colored_msg = Fore.RED + str(msg) + Style.RESET_ALL
        super().error(colored_msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        colored_msg = Fore.LIGHTRED_EX + str(msg) + Style.RESET_ALL
        super().warning(colored_msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        colored_msg = Fore.BLUE + str(msg) + Style.RESET_ALL
        super().warning(colored_msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        colored_msg = Fore.LIGHTGREEN_EX + str(msg) + Style.RESET_ALL
        super().warning(colored_msg, *args, **kwargs)


def __setup_logger(
    file_logger: bool,
    file_logger_level: int,
    console_logger: bool,
    console_logger_level: int,
):
    # init colorama
    init()
    logger = GlobalLogger(__name__)
    # 清除现有的 handler，避免重复添加
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.NOTSET)
    # Set Up Formatter
    # formatter = logging.Formatter(
    #     "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
    # )
    formatter = logging.Formatter("%(message)s")

    if file_logger:
        # Set Up log file name
        current_timestamp = get_current_timestamp()
        logger_file_path_all = f"{convert_to_time(current_timestamp)}.log"
        file_handler = logging.FileHandler(logger_file_path_all, encoding=ENCODE)
        file_handler.setLevel(file_logger_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    if console_logger:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_logger_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


global_logger: Logger = None


def setup_console_file_logger():
    global global_logger
    global_logger = __setup_logger(True, logging.DEBUG, True, logging.DEBUG)


def setup_console_logger():
    global global_logger
    global_logger = __setup_logger(False, logging.DEBUG, True, logging.DEBUG)
