from mauth import GITHUB_TOKEN

from mlogger import global_logger
from json import dumps

import requests
import base64

import mtoken
from mio import get_filename_from_pathall

GITHUB_OWNER = "sony-netapp"
PREFIX_GITHUB_API = f"https://api.github.com/repos/{GITHUB_OWNER}/"


def __get_auth_header(github_user: str = None):
    """Generate authorization header for GitHub API."""
    token = mtoken.get_github_token(github_user) if github_user else GITHUB_TOKEN
    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": "X-GitHub-Api-Version: 2022-11-28",
        "Accept": "application/vnd.github+json",
    }


def __get_auth_header_download(github_user: str = None):
    """Generate authorization header for GitHub API using Basic Authentication."""
    token = mtoken.get_github_token(github_user) if github_user else GITHUB_TOKEN
    return {
        # "Authorization": f"Basic {token}",
        # "User-Agent": "Mozilla/5.0",
        "Authorization": f"Bearer {token}",
        "User-Agent": "X-GitHub-Api-Version: 2022-11-28",
        "Accept": "application/octet-stream",
    }


# -------------------------------- ACCOUNT -----------------------------------


def verify_account(github_user: str = None):
    headers = __get_auth_header(github_user)
    verify_account_url = f"https://api.github.com/octocat"
    response = requests.get(verify_account_url, headers=headers)

    if response.status_code == 200:
        global_logger.info("Account verified successfully.")
    else:
        global_logger.error(
            f"Failed to verify account. Status code: {response.status_code}"
        )


# -------------------------------- RELEASE NOTE -----------------------------------


def create_release_note(repo, release_data, github_user=None):
    headers = __get_auth_header(github_user)
    create_release_url = PREFIX_GITHUB_API + f"{repo}/releases"
    global_logger.info(f"release_note creating in {create_release_url} ...")
    response = requests.post(
        create_release_url, data=dumps(release_data), headers=headers
    )
    if response.status_code == 201:
        global_logger.info("Release created successfully.")
        html_url = response.json()["html_url"]
        release_id = response.json()["id"]
        return [html_url, release_id]
    else:
        global_logger.warning(
            f"Failed to create release.\nStatus code: {response.status_code}"
        )
        global_logger.error(f"Response body: {response.json()}")


def update_release_note_message(
    repo: str, release_id: str, release_note_message: str, github_user=None
):
    headers = __get_auth_header(github_user)
    update_release_note_url = PREFIX_GITHUB_API + f"{repo}/releases/{release_id}"
    global_logger.info(f"release note updating in {update_release_note_url} ...")
    response = requests.patch(
        update_release_note_url,
        data=dumps({"body": release_note_message}),
        headers=headers,
    )
    if response.status_code == 200:
        global_logger.info("Release created successfully.")
    else:
        global_logger.warning(
            f"Failed to create release.\nStatus code: {response.status_code}"
        )
        global_logger.error(f"Response body: {response.json()}")


def get_release_id_by_tag(repo, tag, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/releases/tags/{tag}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        release_data = response.json()
        release_id = release_data.get("id")
        global_logger.debug(f"Found release ID {release_id} for tag '{tag}'.")
        return release_id
    else:
        global_logger.error(
            f"Failed to get release for tag '{tag}'. Status code: {response.status_code}"
        )
        return None


def get_release_note(repo: str, tag_name: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/releases/tags/{tag_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        release_data = response.json()
        return release_data
    else:
        global_logger.error(f"Failed to get release with tag_name {tag_name}.")


def get_release_note_tag_name(repo: str, tag_name: str, github_user: str = None):
    release_data = get_release_note(repo, tag_name, github_user)
    tag_name = release_data.get("tag_name")
    assert tag_name
    return tag_name


def get_release_note_content(repo: str, tag_name: str, github_user: str = None):
    release_data = get_release_note(repo, tag_name, github_user)
    content = release_data.get("body", "")  # 返回 release note 的正文内容
    assert content
    return content


def delete_release_note(repo, release_id, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/releases/{release_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        global_logger.debug(f"Release with ID {release_id} deleted successfully.")
        return True
    else:
        global_logger.error(f"Failed to delete release with ID {release_id}.")
        return False


def get_release_note_of_branch(repo: str, branch, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/releases"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    releases = response.json()

    # 筛选目标分支的 Release
    release_note_list = [
        release for release in releases if release["target_commitish"] == branch
    ]

    return release_note_list


def get_latest_release_note(repo_name, github_user=None) -> str:
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo_name}/releases/latest"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        release_data = response.json()
        return release_data.get("html_url")
    else:
        global_logger.error(
            f"Failed to fetch release info. Status code: {response.status_code}"
        )
        return None


# -------------------------------- ASSETS -----------------------------------

CONTENT_TYPE_RAR = "application/x-rar-compressed"
CONTENT_TYPE_APK = "application/vnd.android.package-archive"


def upload_assets_to_release(
    repo, content_type, release_id, asset_all_path, github_user=None
):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "User-Agent": "X-GitHub-Api-Version: 2022-11-28",
        "Accept": "application/vnd.github+json",
        "Content-Type": content_type,
    }
    asset_name = (
        get_filename_from_pathall(asset_all_path).replace("[", "").replace("]", "-")
    )
    upload_assets_url = f"https://uploads.github.com/repos/{GITHUB_OWNER}/{repo}/releases/{release_id}/assets?name={asset_name}"

    with open(asset_all_path, "rb") as file:
        # BUG: The code below causes CONTENT_TYPE_APK to become ineffective, confusing.
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


def upload_rar_assets_to_release(repo, release_id, asset_all_path, github_user=None):
    upload_assets_to_release(
        repo, CONTENT_TYPE_RAR, release_id, asset_all_path, github_user
    )


def upload_apk_assets_to_release(repo, release_id, asset_all_path, github_user=None):
    upload_assets_to_release(
        repo, CONTENT_TYPE_APK, release_id, asset_all_path, github_user
    )


def get_assets_of_release_note(repo: str, tag_name: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/releases/tags/{tag_name}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        release_data = response.json()
        assets = release_data.get("assets", [])
        assets_dict = {str(asset["id"]): asset["name"] for asset in assets}
        return assets_dict
    elif response.status_code == 404:
        global_logger.error(
            "Release not found. Please check the repository, tag name, or your permissions."
        )
    else:
        global_logger.error(
            f"Failed to fetch release assets. Status code: {response.status_code}"
        )

    return {}


def download_asset_by_id(repo: str, asset_id: str, output_dir=".", github_user=None):
    global_logger.info(
        f"[Download Asset by Id] repo: {repo}, asset_id: {asset_id}, output_dir: {output_dir}, github_user: {github_user}"
    )
    headers = __get_auth_header_download(github_user)
    download_url = (
        f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/releases/assets/{asset_id}"
    )

    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 404:
        raise ValueError(f"Asset with ID {asset_id} not found in repository: {repo}.")
    response.raise_for_status()

    content_disposition = response.headers.get("Content-Disposition", "")
    filename = "unknown_asset"
    if "filename=" in content_disposition:
        filename = content_disposition.split("filename=")[-1].strip('";')

    output_path = f"{output_dir}/{filename}"
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    global_logger.info(f"Downloaded asset to: {output_path}")
    return output_path


# -------------------------------- PULL REQUEST -----------------------------------


def get_pr_base(repo, pull_number, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pull_number}"
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if response.status_code == 200:
        return response_json["base"]["ref"]
    else:
        global_logger.error(f"Failed to get pull request details: {response.content}")
        return None


def get_pr_title(repo: str, pull_number: str, github_user=None) -> str:
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pull_number}"
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        pull_request_json = response.json()
        title = pull_request_json["title"]
        return title
    else:
        global_logger.error(f"Failed to fetch pull requests: {response.status_code}")
        return None


def is_pr_merged(repo: str, pull_number: str, github_user: str = None) -> bool:
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pull_number}/merge"
    response = requests.get(url, headers=headers)

    if response.status_code == 204:
        return True
    elif response.status_code == 404:
        return False
    else:
        response.raise_for_status()


def get_pr_head_sha(repo: str, pull_number: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pull_number}"
    pr_response = requests.get(url, headers=headers)
    assert pr_response
    pr_data = pr_response.json()
    sha = pr_data["head"]["sha"]
    assert sha
    return sha


def get_sha_status(repo: str, sha: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/commits/{sha}/status"
    status_response = requests.get(url, headers=headers)
    status_data = status_response.json()

    # 输出 PR 状态
    state = status_data["state"]
    assert state
    return state


def is_pr_approved(repo: str, pull_number: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pull_number}/reviews"
    response = requests.get(url, headers=headers)
    reviews = response.json()

    for review in reviews:
        if review["state"] == "APPROVED":
            return True
    return False


def merge_pr(repo, pull_number, github_user: str = None):
    base_branch = get_pr_base(repo, pull_number, github_user)
    assert base_branch

    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pull_number}/merge"

    commit_title = (
        f"Merge pull request #{pull_number} from {GITHUB_OWNER}/{base_branch}"
    )
    commit_message = f"Automatically merging PR #{pull_number} from {base_branch}."

    payload = {
        "commit_title": commit_title,
        "commit_message": commit_message,
        "merge_method": "merge",
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        global_logger.debug("PR has been successfully merged.")
        return True
    elif response.status_code == 405:
        global_logger.warning("PR could not be merged (there may be conflicts).")
        return False
    else:
        global_logger.warning(
            f"Request failed with status code: {response.status_code}"
        )
        global_logger.warning(response.json())
        return False


def get_latest_merged_pr_for_branch(repo, branch_name, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls"
    params = {
        "state": "closed",  # Only closed PRs can be merged
        "base": branch_name,  # Filter by branch
        "per_page": 100,  # Maximize results per page
    }

    latest_pr = None
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={**params, "page": page})

        if response.status_code != 200:
            global_logger.error(
                f"Error fetching PRs: {response.status_code}, {response.text}"
            )
            return None

        prs = response.json()
        if not prs:
            break  # No more PRs to process
        latest_10_pr = prs[:10]
        # Check if PR is merged
        for pr in latest_10_pr:
            # Get details of the individual PR to check for 'merged'
            pr_details_url = pr["url"]
            pr_details_response = requests.get(pr_details_url, headers=headers)
            pr_details = pr_details_response.json()

            if pr_details.get("merged_at"):  # Check if the PR is merged
                if (
                    latest_pr is None
                    or pr_details["merged_at"] > latest_pr["merged_at"]
                ):
                    latest_pr = pr_details

        page += 1  # Move to next page of results

    return latest_pr["html_url"], latest_pr["number"] if latest_pr else None


# -------------------------------- PR CICD -----------------------------------


def is_pr_runs_succeed(repo: str, pull_number: str, github_user: str = None):
    head_sha = get_pr_head_sha(repo, pull_number, github_user)
    sha_status = get_sha_status(repo, head_sha, github_user)
    return sha_status == "success"


def get_pr_runs_details(repo: str, commit_sha: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    check_runs_url = PREFIX_GITHUB_API + f"{repo}/commits/{commit_sha}/check-runs"
    print(check_runs_url)
    check_runs_response = requests.get(check_runs_url, headers=headers)
    if check_runs_response.status_code != 200:
        raise global_logger.error(
            f"Error fetching check runs: {check_runs_response.status_code}, {check_runs_response.text}"
        )

    check_runs_data = check_runs_response.json()
    print(check_runs_data)
    # Step 3: Extract the details URL for each check run
    details_urls = []
    for check_run in check_runs_data.get("check_runs", []):
        details_urls.append(
            {
                "name": check_run["name"],
                "details_url": check_run["details_url"],
                "status": check_run["status"],
                "conclusion": check_run.get("conclusion", "in_progress"),
            }
        )

    return check_runs_data


def get_pr_runs_artifacts(repo: str, run_id: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    artifacts_url = PREFIX_GITHUB_API + f"{repo}/actions/runs/{run_id}/artifacts"
    print(artifacts_url)
    response = requests.get(artifacts_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch artifacts. Status Code: {response.status_code}")
        return None

    artifacts = response.json().get("artifacts", [])
    return artifacts


# -------------------------------- TAG -----------------------------------


def is_github_tag_exists(repo, tag, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/git/refs/tags/{tag}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False


def delete_github_tag(repo, tag_name, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/git/refs/tags/{tag_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        global_logger.debug(f"Tag {tag_name} deleted successfully.")
        return True
    else:
        global_logger.error(f"Failed to delete tag {tag_name}.")
        return False


# -------------------------------- COMMIT -----------------------------------


def get_latest_commit_for_branch(repo, branch, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/branches/{branch}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # 解析 JSON 响应并提取最新的 commit SHA 值
        commit = response.json()
        return commit
    else:
        raise global_logger.error(f"Error: {response.status_code}, {response.text}")


def get_latest_commit_sha_for_branch(repo, branch, github_user=None):
    commit = get_latest_commit_for_branch(repo, branch)
    commit_sha = commit["commit"]["sha"]
    return commit_sha


def get_commits_for_pr(repo, pr_number, github_user=None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/pulls/{pr_number}/commits"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise global_logger.error(
            f"Failed to fetch commits for PR #{pr_number}. Error: {response.status_code}"
        )
    commits = response.json()
    return commits


def get_latest_commit_sha_for_pr(repo, pr_number, github_user=None):
    commits = get_commits_for_pr(repo, pr_number, github_user)
    commit_shas = [commit["sha"] for commit in commits]
    return commit_shas[-1]


def get_commit_sha_for_tag(repo: str, tag_name: str, github_user: str = None):
    headers = __get_auth_header(github_user)
    url = PREFIX_GITHUB_API + f"{repo}/git/ref/tags/{tag_name}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch tag information")

    tag_info = response.json()
    commit_sha = tag_info["object"]["sha"]
    commit_url = tag_info["object"]["url"]

    return commit_sha


# -------------------------------- FILE -----------------------------------


def get_github_file_content(repo, branch, file_path, github_user=None):
    url = PREFIX_GITHUB_API + f"{repo}/contents/{file_path}?ref={branch}"
    headers = __get_auth_header(github_user)
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        data = response.json()
        # Get and decode the file content (Base64)
        file_content = base64.b64decode(data["content"]).decode("utf-8")
        global_logger.debug(
            f"successfully to get file > {file_path} from repo > {repo} branch > {branch}"
        )
        return file_content
    else:
        global_logger.error(
            f"Unable to retrieve file content, HTTP status code: {response.status_code}"
        )
        return None
