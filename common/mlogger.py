from mstr import ENCODE
from logging import Logger

import logging
from colorama import init, Fore, Style

from mtime import get_current_timestamp, convert_to_time


class ErrorInLogger(Exception):
    def __init__(self, message):
        self.message = message


# warn() 方法： 在早期版本的 Python 中，warn() 方法用于记录警告级别的日志消息。然而，自从 Python 2.6 版本开始，warn() 方法已经被废弃，并建议使用 warning() 方法代替。尽管 warn() 方法在大多数情况下仍然可用，但它在未来的 Python 版本中可能会被移除。
# warning() 方法： warning() 方法用于记录警告级别的日志消息，它是 logger 模块的一个方法。与 warn() 方法相比，warning() 方法更加标准化和推荐，因此在编写新代码时应该优先选择使用 warning() 方法来记录警告级别的日志消息。


class GlobalLogger(logging.Logger):
    def error(self, msg, *args, **kwargs):
        super().error(msg, *args, **kwargs)
        print(Fore.RED + str(msg) + Style.RESET_ALL)

    def warning(self, msg, *args, **kwargs):
        super().warning(msg, *args, **kwargs)
        print(Fore.LIGHTRED_EX + str(msg) + Style.RESET_ALL)


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
    formatter = logging.Formatter("%(funcName)s - %(levelname)s - %(message)s")
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
