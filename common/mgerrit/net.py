from mlogger import global_logger

import requests
import base64
import json

import mstr
import mauth

# documentation: https://www.tool.sony.biz/tv-gerrit/Documentation/rest-api.html

GERRIT_SITE = "https://www.tool.sony.biz/tv-gerrit"
GERRIT_USERNAME = "5109U25854"
GERRIT_PASSWORD = "n6kxYZwUKM8idgzO7ILpnhm+U/wJPcX2qkmhUfwxvg"
# CREDENTIALS = base64.b64encode(f"{GERRIT_USERNAME}:{GERRIT_PASSWORD}".encode()).decode()

EMAIL_BINYU = "Binyu.Ren@sony.com"
EMAIL_CHERRY = "Yanjing.Wu@sony.com"

NAME_JENKINS = "BoC Checker"
KEYWORDS_STATRED = "Build started"
KEYWORDS_FINISHED = "Fullbuild"
KEYWORDS_OK = "OK"
KEYWORDS_FAIL = "FAIL"
KEYWORDS_BOC_LINK = "boc_sony"


def __get_clean_response(string: str):
    # string = raw_string.decode("unicode_escape").strip("b ')]}\n")
    # if string.strip()[-1] != "}":
    #     string += "}"
    # string = string.replace("\n", "\\n")
    # return loads(string)
    # Ensure the string is decoded to a regular string if it's in bytes
    if isinstance(string, bytes):
        string = string.decode("utf-8")

    # Remove Gerrit specific prefix
    if string.startswith(")]}'"):
        string = string[4:].strip()

    # Check if the string is not empty after cleanup
    if not string:
        raise ValueError("Empty response received after removing Gerrit prefix")

    try:
        return json.loads(string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}") from e


def __get_commit_message_from_commit(commit_data):
    return commit_data.get("message")


# ------------------------------------------ HTTP Basic ---------------------------------------------


def __get_auth_header():
    """Generate authorization header for GitHub API."""
    # gerrit_password = (
    #     mtoken.get_gerrit_password(gerrit_user) if gerrit_user else GERRIT_PASSWORD
    # )
    credentials = base64.b64encode(
        f"{mauth.GERRIT_USER}:{mauth.GERRIT_PASS}".encode()
    ).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json; charset=UTF-8",
    }


def __get_gerrit(url):
    global_logger.debug(f"GET gerrit rest api data from:{url}")
    headers = __get_auth_header()
    response = requests.get(
        url,
        headers=headers,
    )
    if response.status_code == 200:
        global_logger.debug("succeed to GET gerrit")
        return __get_clean_response(response.content)
    else:
        global_logger.error(
            f"failed to GET gerrit: {response.status_code}\nreponse message: {response.content}"
        )


def __post_gerrit(url, json_data):
    global_logger.debug(f"POST gerrit rest api to:{url}")
    headers = __get_auth_header()
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code == 200:
        global_logger.debug("succeed to POST gerrit")
        return response.content
    else:
        global_logger.error(
            f"failed to POST gerrit: {response.status_code}\nreponse message: {response.content}"
        )


def __put_gerrit(url, json_data):
    global_logger.debug(f"PUT gerrit rest api to:{url}")
    headers = __get_auth_header()
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code == 200:
        global_logger.debug("succeed to PUT gerrit")
        return response.content
    else:
        global_logger.error(
            f"failed to PUT gerrit: {response.status_code}\nreponse message: {response.content}"
        )


# ------------------------------------------ Commit Seq ---------------------------------------------


def get_api_change_id_by_commit_seq(commit_seq: str) -> str:
    url = f"{GERRIT_SITE}/a/changes/{commit_seq}"
    results = __get_gerrit(url)
    api_change_id = results["id"]
    return api_change_id


# ------------------------------------------ Api Change Id ---------------------------------------------


def get_change_common(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}"
    response_str = __get_gerrit(url)
    return response_str


def get_change_detail(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/detail"
    response_str = __get_gerrit(url)
    return response_str


def get_change_comments(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/messages"
    response_str = __get_gerrit(url)
    return response_str


def is_boc_started(api_change_id):
    comment_list = get_change_comments(api_change_id)
    for comment in comment_list:
        if NAME_JENKINS == comment.get("author").get("name"):
            message = comment.get("message")
            if KEYWORDS_STATRED in message:
                global_logger.debug(f"boc is started in change:{api_change_id}")
                return True
    global_logger.debug(f"boc has not started in change:{api_change_id}")
    return False


def is_boc_finished(api_change_id):
    comment_list = get_change_comments(api_change_id)
    for comment in comment_list:
        if NAME_JENKINS == comment.get("author").get("name"):
            message = comment.get("message")
            if KEYWORDS_FINISHED in message:
                if KEYWORDS_OK in message:
                    global_logger.debug(f"boc build succeed in change: {api_change_id}")
                    return True
                elif KEYWORDS_FAIL in message:
                    global_logger.warning(
                        f"boc build failed in change: {api_change_id}"
                    )
                    return False
    return None


def get_boc_link_list_finished(api_change_id):
    comment_list = get_change_comments(api_change_id)
    boc_link_list = []
    for comment in comment_list:
        if NAME_JENKINS == comment.get("author").get("name"):
            message = comment.get("message")
            if KEYWORDS_FINISHED in message:
                if KEYWORDS_OK in message:
                    web_link_list = mstr.extract_web_link_list(message)
                    for web_link in web_link_list:
                        if KEYWORDS_BOC_LINK in web_link:
                            boc_link_list.append(web_link)
                elif KEYWORDS_FAIL in message:
                    global_logger.warning(f"boc build failed!")
    return boc_link_list


def get_boc_link_list_started(api_change_id):
    comment_list = get_change_comments(api_change_id)
    boc_link_list = []
    for comment in comment_list:
        if NAME_JENKINS == comment.get("author").get("name"):
            message = comment.get("message")
            if KEYWORDS_STATRED in message:
                web_link_list = mstr.extract_web_link_list(message)
                for web_link in web_link_list:
                    if KEYWORDS_BOC_LINK in web_link:
                        boc_link_list.append(web_link)
    return boc_link_list


def get_change_check(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/check"
    response_str = __get_gerrit(url)
    return response_str


def get_current_revision_commit(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/revisions/current/commit"
    response_str = __get_gerrit(url)
    return response_str


def get_current_revision_commit_msg(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/revisions/current/commit"
    response_str = __get_gerrit(url)
    commit_msg = __get_commit_message_from_commit(response_str)
    return commit_msg


def add_reviewer(api_change_id, reviewer_email):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/reviewers"
    json_reviewers = {"reviewer": reviewer_email}
    results = __post_gerrit(url, json_reviewers)
    return results


def add_cc(api_change_id, cc_email):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/cc"
    json_reviewers = {"reviewer": cc_email}
    results = __post_gerrit(url, json_reviewers)
    return results


def reply_verify(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/revisions/current/review"
    # json_reply = {"labels": {"Code-Review": "-1"}}
    json_reply = {"message": "BOC & DQA Check OK", "labels": {"Verified": 1}}
    results = __post_gerrit(url, json_reply)
    return results


def update_commit_message(api_change_id, commit_message):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/revisions/current/commit_message"
    return __put_gerrit(url, {"message": commit_message})


def is_commit_verified(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/revisions/current/review"
    results = __get_gerrit(url)
    verified_data = results["labels"]["Verified"]["all"]
    for reviewer in verified_data:
        if reviewer["value"] == 1:
            global_logger.info(f"Verified +1 found by {reviewer['name']}")
            return True
    global_logger.info("No Verified +1 found.")
    return False


def is_commit_code_review_2(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/revisions/current/review"
    results = __get_gerrit(url)
    code_review = results["labels"]["Code-Review"]["all"]
    for review in code_review:
        if review["value"] == 2:
            global_logger.info(f"Code-Review+2 by: {review['name']}")
            return True
    global_logger.info("No Code-Review+2 found.")
    return False


def is_commit_merged(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/detail"
    results = __get_gerrit(url)
    status = results["status"]
    if status == "MERGED":
        global_logger.info(f"Change {api_change_id} is merged.")
        return True
    else:
        global_logger.info(f"Change {api_change_id} is not merged. Status: {status}")
        return False


def merge_commit(api_change_id):
    url = f"{GERRIT_SITE}/a/changes/{api_change_id}/submit"
    results = __post_gerrit(url, {})
    return results
