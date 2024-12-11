from mlogger import global_logger

import re

PATTERN_COMMIT_ID = r"Change-Id: (\S+)"
PATTERN_GERRIT_LINK = r"https://www\.tool\.sony\.biz/tv-gerrit/[\S]+"
PATTERN_GERRIT_SEQ = r"^https://www\.tool\.sony\.biz/tv-gerrit/c/.+/\+/(\d+)$"


def extract_change_id_from_git_msg(commit_message: str):
    match = re.search(PATTERN_COMMIT_ID, commit_message)
    if match:
        change_id = match.group(1)
        return change_id
    else:
        global_logger.warning(f"cannot found change id in message: {commit_message}")


def extract_commit_seq_from_url(url: str) -> str:
    match = re.search(PATTERN_GERRIT_SEQ, url)
    if match:
        return match.group(1)
    return None


def extract_gerrit_link_list(text: str):
    links = re.findall(PATTERN_GERRIT_LINK, text)
    return links


PATTERN_API_CHANGEID = "sony/android/vendor/sony/prebuilts/packages/apps/{submit_repo}~{submit_branch}~{change_id}"


def format_api_change_id(submit_repo, submit_branch, change_id):
    if submit_branch and submit_repo and change_id:
        api_change_id = PATTERN_API_CHANGEID.format(
            submit_repo=submit_repo, submit_branch=submit_branch, change_id=change_id
        )
        api_change_id = api_change_id.replace("/", "%2F")
        return api_change_id
    else:
        global_logger.warning(
            f"any value is empty! submit_repo:{submit_repo} submit_branch:{submit_branch} change_id:{change_id}"
        )
