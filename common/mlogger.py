from mstr import ENCODE

import logging
import os
import sys
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


def setup_logger():
    # init colorama
    init()
    logger = GlobalLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
    )
    current_timestamp = get_current_timestamp()
    logger_file_path_all = f"{convert_to_time(current_timestamp)}.log"
    file_handler = logging.FileHandler(logger_file_path_all, encoding=ENCODE)
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


global_logger = setup_logger()
