from dataclasses import dataclass
from mlogger import global_logger
import mio
import mcrypt
import mtime
import minput
import mlogger
import mprint

CONFIG_FILE = "//43.82.125.244/ChinaUX/.auto/config/tokens.json"


@dataclass
class Token:
    encrypted_token: str
    expired_timestamp: int = None  # Optional field, default is None


TOKEN_DICT = mio.get_json_from_file(CONFIG_FILE)


def get_token(user: str, platform: str, enter_token_func) -> str:
    """
    General method to get a token. Retrieves the token for a given user and platform.
    If the token does not exist or is expired, calls `enter_token_func` to get a new token.
    """
    if user not in TOKEN_DICT:
        global_logger.warning(f"{user} not existing in token config")
        return enter_token_func()

    user_token = TOKEN_DICT[user]
    if platform not in user_token:
        global_logger.warning(f"{platform} not existing in user config")
        return enter_token_func()

    token = user_token[platform]
    if "expired_timestamp" in token:
        current_timestamp = mtime.get_current_timestamp()
        if current_timestamp > token["expired_timestamp"]:
            global_logger.warning(f"{platform} token has expired")
            return enter_token_func()

    encrypted_token = token["encrypted_token"]
    return mcrypt.decrypt(encrypted_token)


def set_token(
    user: str, platform: str, plain_token: str, expiry_days: int = None
) -> bool:
    """
    General method to set a token. Encrypts and stores the token, with optional expiration.
    """
    encrypted_token = mcrypt.encrypt(plain_token)
    token = {"encrypted_token": encrypted_token}

    if expiry_days:
        current_timestamp = mtime.get_current_timestamp()
        token["expired_timestamp"] = mtime.get_timestamp_after_days(
            current_timestamp, expiry_days
        )

    # Ensure we don't overwrite other platform tokens
    if user not in TOKEN_DICT:
        TOKEN_DICT[user] = {}
    TOKEN_DICT[user][platform] = token

    mio.write_json_to_file(CONFIG_FILE, TOKEN_DICT)
    return True


def enter_for_token(
    user: str, platform_name: str, url: str, expiry_days: int = None
) -> str:
    """
    General method to input a token. The user manually inputs the token, which is then saved.
    """
    mprint.printc_web_link(
        "请输入以下页面生成的token/http credentials, 尽量放大权限, 选择不过期", url
    )
    plain_token = minput.input_para(platform_name + ": ")
    if not plain_token:
        global_logger.error(f"Input {platform_name} token is empty!")
        return None

    set_token(user, platform_name, plain_token, expiry_days)
    return plain_token


# CSC JIRA-specific implementation
def get_csc_jira_token(user: str) -> str:
    return get_token(
        user,
        "csc_jira",
        lambda: enter_for_token(
            user,
            "csc_jira",
            "https://csc-jira.sony.com.cn/secure/ViewProfile.jspa",
        ),
    )


# TOKYO JIRA-specific implementation
def get_tokyo_jira_token(user: str) -> str:
    return get_token(
        user,
        "sony_jira",
        lambda: enter_for_token(
            user,
            "sony_jira",
            "https://www.tool.sony.biz/tv-jira/secure/ViewProfile.jspa",
            189,
        ),
    )


# GitHub-specific implementation
def get_github_token(user: str) -> str:
    return get_token(
        user,
        "github",
        lambda: enter_for_token(
            user,
            "github",
            "https://github.com/settings/tokens",
        ),
    )


# Gerrit-specific implementation
def get_gerrit_password(user: str) -> str:
    return get_token(
        user,
        "gerrit",
        lambda: enter_for_token(
            user,
            "gerrit",
            "https://www.tool.sony.biz/tv-gerrit/settings/#HTTPCredentials",
        ),
    )
