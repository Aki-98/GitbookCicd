import re
import string
import random

from common import mio

ENCODE = "UTF-8"
PATTERN_WEB = r"https?://\S+"
CHARACTERS_ALPHANUMERIC = string.ascii_letters + string.digits


def generate_random_alphanumeric(length=11):
    random_string = "".join(
        random.choice(CHARACTERS_ALPHANUMERIC) for _ in range(length)
    )
    return random_string


PATTERN_ALPHANUMERIC = r"^[a-zA-Z0-9]{11}$"


def is_valid_alphanumeric(file_path: str) -> bool:
    file_basename = mio.get_basename(file_path)
    return bool(re.match(PATTERN_ALPHANUMERIC, file_basename))


def extract_web_link_list(str):
    str = str.strip()
    matches = re.findall(PATTERN_WEB, str)
    return matches
