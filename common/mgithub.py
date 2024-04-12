from mauth import GITHUB_USER, GITHUB_OWNER, GITHUB_TOKEN

import re
import requests
from json import dumps

from mio import get_filename_from_pathall
from mlogger import global_logger


def verify_account():
    headers = {
        "Authorization": f"Authorization Bearer {GITHUB_TOKEN}",
        "User-Agent": "X-GitHub-Api-Version: 2022-11-28",
    }

    verify_account_url = f"https://api.github.com/octocat"
    response = requests.get(verify_account_url, headers=headers)

    if response.status_code == 200:
        global_logger.info("Account verified successfully.")
    else:
        global_logger.error(
            f"Failed to verify account. Status code: {response.status_code}"
        )


def create_release_note(repo, release_data):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "User-Agent": "X-GitHub-Api-Version: 2022-11-28",
        "Accept": "application/vnd.github+json",
    }
    create_release_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/releases"
    global_logger.info("ReleaseNote has been created: " + create_release_url)
    response = requests.post(
        create_release_url, data=dumps(release_data), headers=headers
    )

    if response.status_code == 201:
        global_logger.info("Release created successfully.")
        html_url = response.json()["html_url"]
        release_id = response.json()["id"]
        return [html_url, release_id]
    else:
        global_logger.error(
            f"Failed to create release. Status code: {response.status_code}"
        )
        global_logger.error(response)
        return None


def get_tag_name_from_release_note(repo, release_id):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/releases/{release_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        release_data = response.json()
        tag_name = release_data.get("tag_name")
        global_logger.debug(f"Tag_name of release with ID {release_id} is: {tag_name}")
        return tag_name
    else:
        global_logger.error(f"Failed to get release with ID {release_id}.")
        return None


def delete_release_note(repo, release_id):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/releases/{release_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        global_logger.debug(f"Release with ID {release_id} deleted successfully.")
        return True
    else:
        global_logger.error(f"Failed to delete release with ID {release_id}.")
        return False


CONTENT_TYPE_RAR = "application/x-rar-compressed"
CONTENT_TYPE_APK = "application/vnd.android.package-archive"


def upload_assets_to_release(repo, content_type, release_id, asset_all_path):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "User-Agent": "X-GitHub-Api-Version: 2022-11-28",
        "Accept": "application/vnd.github+json",
        "Content-Type": content_type,
    }
    asset_name = get_filename_from_pathall(asset_all_path)
    upload_assets_url = f"https://uploads.github.com/repos/{GITHUB_OWNER}/{repo}/releases/{release_id}/assets?name={asset_name}"

    with open(asset_all_path, "rb") as file:
        # 下面的代码导致了CONTENT_TYPE_APK失效，迷
        # files = {"file": (asset_all_path, file)}
        # response = post(upload_assets_url, headers=headers, files=files)
        response = requests.post(upload_assets_url, headers=headers, data=file)

    if response.status_code == 201:
        global_logger.info("Asset uploaded successfully")
        return True
    else:
        global_logger.error(
            f"Failed to upload asset. Status code: {response.status_code}"
        )
        global_logger.error(response)
        return False


def upload_rar_assets_to_release(repo, release_id, asset_all_path):
    upload_assets_to_release(repo, CONTENT_TYPE_RAR, release_id, asset_all_path)


def upload_apk_assets_to_release(repo, release_id, asset_all_path):
    upload_assets_to_release(repo, CONTENT_TYPE_APK, release_id, asset_all_path)


def get_pull_request_base(repo, pull_number):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/pulls/{pull_number}"
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if response.status_code == 200:
        return response_json["base"]["ref"]
    else:
        global_logger.error(f"Failed to get pull request details: {response.content}")
        return None


def delete_github_tag(repo, tag_name):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/git/refs/tags/{tag_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        global_logger.debug(f"Tag {tag_name} deleted successfully.")
        return True
    else:
        global_logger.error(f"Failed to delete tag {tag_name}.")
        return False


PATTERN_PULL_REQUEST = r"https://github\.com/.*?/pull/\d+"


def extract_pull_request_link(str):
    str = str.strip()
    matches = re.findall(PATTERN_PULL_REQUEST, str)
    return matches


def extract_pull_request_number(str):
    str = str.strip()
    match = re.search(PATTERN_PULL_REQUEST, str)
    if match:
        pull_request_number = match.group(1)
        global_logger.debug(f"The pull request number is: {pull_request_number}")
        return pull_request_number
    else:
        global_logger.debug("No pull request number found.")
        return None
