from mstr import extract_web_link_list, extract_pr_list
from mlogger import global_logger

import platform
import subprocess

import mterminal
import mtime


# --------------------------------------- Str Only -------------------------------------


# Get Gerrit's RefsBranch
def __get_refs_branch(branch: str) -> str:
    refs_branch = f"{branch}:refs/for/{branch}"
    return refs_branch


# --------------------------------------- mTerminal Only -------------------------------------


def show_clean_untracked_files(repo_path: str) -> bool:
    global_logger.info(f"Calling show_clean_untracked_files on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "clean", "-nXfd"])


def clean_untracked_files(repo_path: str) -> bool:
    global_logger.info(f"Calling clean_untracked_files on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "clean", "-Xfd"])


def show_latest_node(repo_path: str) -> bool:
    global_logger.info(f"Calling show_latest_node on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "log", "-1"])


def reset_node_remote(repo_path: str, branch_name: str) -> bool:
    global_logger.info(
        f"Calling reset_node_remote on repo_path: {repo_path} branch_name: {branch_name}"
    )
    return mterminal.run_command(
        repo_path, ["git", "reset", "--hard", f"origin/{branch_name}"]
    )


def reset_node_local(repo_path: str) -> bool:
    global_logger.info(f"Calling reset_node_local on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "reset", "--hard", f"^HEAD"])


def remove_untracked_files(repo_path: str) -> bool:
    global_logger.info(f"Calling remove_untracked_files on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "clean", "-f", "-d"])


def update_repo(repo_path: str) -> bool:
    global_logger.info(f"Calling update_repo on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "pull", "origin"])


def checkout_to_target_branch(repo_path: str, branch_name: str) -> bool:
    global_logger.info(
        f"Calling checkout_to_target_branch on repo_path: {repo_path} branch_name: {branch_name}"
    )
    return mterminal.run_command(repo_path, ["git", "checkout", branch_name])


def remove_local_branch(repo_path: str, branch_name: str) -> bool:
    global_logger.info(
        f"Calling remove_local_branch on repo_path: {repo_path} branch_name: {branch_name}"
    )
    return mterminal.run_command(repo_path, ["git", "branch", "-D", branch_name])


def remove_remote_branch(repo_path: str, branch_name: str) -> bool:
    global_logger.info(
        f"Calling remove_local_branch on repo_path: {repo_path} branch_name: {branch_name}"
    )
    return mterminal.run_command(
        repo_path, ["git", "push", "origin", "--delete", branch_name]
    )


def checkout_to_new_branch(repo_path: str, new_branch_name: str) -> bool:
    global_logger.info(
        f"Calling checkout_to_new_branch on repo_path: {repo_path} new_branch_name: {new_branch_name}"
    )
    return mterminal.run_command(repo_path, ["git", "checkout", "-b", new_branch_name])


def add_all_files(repo_path: str) -> str:
    global_logger.info(f"Calling add_all_files on repo_path: {repo_path}")
    return mterminal.run_command(repo_path, ["git", "add", "."])


def add_certain_file(repo_path: str, file_path: str) -> bool:
    global_logger.info(
        f"Calling add_certain_file on repo_path: {repo_path} file_path: {file_path}"
    )
    return mterminal.run_command(repo_path, ["git", "add", file_path])


def commit_by_message(repo_path: str, commit_message: str) -> bool:
    global_logger.info(
        f"Calling commit_by_message on repo_path: {repo_path} commit_message: {commit_message}"
    )
    return mterminal.run_command(
        repo_path, ["git", "commit", "-m", f'"{commit_message}"']
    )


def delete_husky(repo_path: str) -> bool:
    global_logger.info(f"Calling delete_husky on repo_path: {repo_path}")
    if platform.system() == "Windows":
        global_logger.debug("Detected that executing machine is in windows platform")
        is_file_deleted = mterminal.run_command(repo_path, ["rm", ".husky/commit-msg"])
        is_folder_deleted = mterminal.run_command(repo_path, ["rmdir", ".husky"])
        return is_file_deleted and is_folder_deleted
    elif platform.system() == "Linux":
        global_logger.debug("Detected that executing machine is in ubuntu platform")
        return mterminal.run_command(repo_path, ["rm", "-r", ".husky/"])


def commit_by_txt(repo_path: str, txt_name: str) -> bool:
    global_logger.info(
        f"Calling commit_by_txt on repo_path: {repo_path} txt_name: {txt_name}"
    )
    return mterminal.run_command(repo_path, ["git", "commit", "-F", txt_name])


# --------------------------------------- subprocess -------------------------------------


def push_to_branch_dict(repo_path: str, branch_name: str) -> dict:
    """
    Pushes changes to the specified branch and detects various failure conditions.
    :param repo_path: Path to the local Git repository.
    :param branch_name: Target branch to push changes to.
    :return: A dictionary with status and optional additional information.
    """

    global_logger.info(
        f"Calling push_to_branch on repo_path: {repo_path}, branch_name: {branch_name}"
    )

    # Run the `git push` command
    try:
        result = subprocess.run(
            ["git", "push", "origin", branch_name],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the raw output
        global_logger.debug(f"Git push output:\n{result.stdout}\n{result.stderr}")

        # Check if the push was successful
        if result.returncode == 0:
            global_logger.info("Push to branch succeeded.")
            web_links = extract_web_link_list(result.stdout)
            return {"status": "success", "web_links": web_links}

        # Handle specific errors
        stderr = result.stderr.lower()

        if "could not resolve host" in stderr:
            global_logger.error("Network error: Could not resolve host.")
            return {
                "status": "error",
                "error_type": "network",
                "message": "Could not resolve host.",
            }

        if "connection timed out" in stderr:
            global_logger.error("Network error: Connection timed out.")
            return {
                "status": "error",
                "error_type": "network",
                "message": "Connection timed out.",
            }

        if "failed to push some refs" in stderr:
            if "fetch first" in stderr or "non-fast-forward" in stderr:
                global_logger.error("Push rejected: Non-fast-forward update required.")
                return {
                    "status": "error",
                    "error_type": "non_fast_forward",
                    "message": "Push rejected: Non-fast-forward update required. Fetch and merge first.",
                }
            elif "remote rejected" in stderr:
                global_logger.error("Push rejected by the remote server.")
                return {
                    "status": "error",
                    "error_type": "remote_rejection",
                    "message": "Push rejected by the remote server.",
                }

        # Catch-all for unknown errors
        global_logger.error(f"Unknown push error: {stderr.strip()}")
        return {"status": "error", "error_type": "unknown", "message": stderr.strip()}

    except Exception as e:
        global_logger.exception("An exception occurred during git push.")
        return {"status": "error", "error_type": "exception", "message": str(e)}


def push_pr_branch(repo_path: str, pr_branch: str) -> dict:
    """
    Pushes a branch to the remote with --set-upstream and detects various failure conditions.
    :param repo_path: Path to the local Git repository.
    :param pr_branch: Name of the branch to push.
    :return: A dictionary with status and optional additional information.
    """

    global_logger.info(
        f"Calling push_pr_branch on repo_path: {repo_path}, pr_branch: {pr_branch}"
    )

    try:
        # Run the `git push --set-upstream` command
        result = subprocess.run(
            ["git", "push", "origin", "--set-upstream", pr_branch],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the raw output
        global_logger.debug(f"Git push output:\n{result.stdout}\n{result.stderr}")

        # Check if the push was successful
        if result.returncode == 0:
            global_logger.info("Push PR branch succeeded.")
            web_links = extract_web_link_list(result.stdout)
            return {"status": "success", "web_links": web_links}

        # Handle specific errors
        stderr = result.stderr.lower()

        if "could not resolve host" in stderr:
            global_logger.error("Network error: Could not resolve host.")
            return {
                "status": "error",
                "error_type": "network",
                "message": "Could not resolve host.",
            }

        if "connection timed out" in stderr:
            global_logger.error("Network error: Connection timed out.")
            return {
                "status": "error",
                "error_type": "network",
                "message": "Connection timed out.",
            }

        if "failed to push some refs" in stderr:
            if "fetch first" in stderr or "non-fast-forward" in stderr:
                global_logger.error("Push rejected: Non-fast-forward update required.")
                return {
                    "status": "error",
                    "error_type": "non_fast_forward",
                    "message": "Push rejected: Non-fast-forward update required. Fetch and merge first.",
                }
            elif "remote rejected" in stderr:
                global_logger.error("Push rejected by the remote server.")
                return {
                    "status": "error",
                    "error_type": "remote_rejection",
                    "message": "Push rejected by the remote server.",
                }

        # Catch-all for unknown errors
        global_logger.error(f"Unknown push error: {stderr.strip()}")
        return {"status": "error", "error_type": "unknown", "message": stderr.strip()}

    except Exception as e:
        global_logger.exception("An exception occurred during git push.")
        return {"status": "error", "error_type": "exception", "message": str(e)}


def get_last_commit_message(repo_path: str) -> str:
    """
    Retrieves the last commit message from the specified repository.
    :param repo_path: Path to the local Git repository.
    :return: A dictionary with the status and the commit message or error details.
    """

    global_logger.info(f"Calling get_last_commit_message on repo_path: {repo_path}")

    try:
        # Run the `git log` command to get the last commit message
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the raw output
        if result:
            global_logger.debug(f"Git log output:\n{result.stdout}\n{result.stderr}")

        if result.returncode == 0:
            # Successfully retrieved the commit message
            commit_message = result.stdout.strip()
            global_logger.info(f"Last commit message: {commit_message}")
            return commit_message
        else:
            # Failed to retrieve the commit message
            error_message = result.stderr.strip()
            global_logger.error(f"Failed to get last commit message: {error_message}")
            return None

    except Exception as e:
        global_logger.exception(
            "An exception occurred while retrieving the last commit message."
        )
        return None


def setup_remote_repo_safe_dir(repo_path_remote: str) -> dict:
    """
    Initializes a remote repository by ensuring it is added to the Git safe.directory configuration.
    :param repo_path_remote: Path to the remote repository to initialize.
    :return: A dictionary with the status and any relevant information or errors.
    """

    global_logger.info(
        f"Calling workflow_init_remote_repo on repo_path_remote: {repo_path_remote}"
    )

    try:
        # Check if the repo path is already in safe.directory
        already_exist = False
        result_check = subprocess.run(
            ["git", "config", "--global", "--get-all", "safe.directory"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        global_logger.debug(
            f"Checking existing safe.directory:\n{result_check.stdout}\n{result_check.stderr}"
        )

        if result_check.returncode != 0:
            error_message = result_check.stderr.strip()
            global_logger.error(f"Error checking safe.directory: {error_message}")
            return {"status": "error", "message": error_message}

        if repo_path_remote in result_check.stdout:
            # Repo already exists in safe.directory
            already_exist = True
            global_logger.debug(
                f"Repo > {repo_path_remote} already exists in safe.directory of .gitconfig"
            )
            return {
                "status": "already_exist",
                "message": "Repo already in safe.directory",
            }

        # Add the repo to safe.directory
        if not already_exist:
            result_add = subprocess.run(
                [
                    "git",
                    "config",
                    "--global",
                    "--add",
                    "safe.directory",
                    repo_path_remote,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            global_logger.debug(
                f"Adding repo to safe.directory:\n{result_add.stdout}\n{result_add.stderr}"
            )

            if result_add.returncode == 0:
                global_logger.info(
                    f"Repo > {repo_path_remote} successfully added to safe.directory"
                )
                return {
                    "status": "add_successfully",
                    "message": "Repo added to safe.directory",
                }
            else:
                error_message = result_add.stderr.strip()
                global_logger.error(
                    f"Error adding repo to safe.directory: {error_message}"
                )
                return {"status": "error", "message": error_message}

    except Exception as e:
        global_logger.exception(
            "An exception occurred while initializing the remote repository."
        )
        return {"status": "error", "message": str(e)}


def check_tag_exists(repo_path: str, tag_name: str) -> dict:
    """
    Check if a specific tag exists in a Git repository.

    Args:
        repo_path (str): The path to the Git repository.
        tag_name (str): The name of the tag to check.

    Returns:
        dict: A dictionary containing the status (success or error) and the result or error message.
    """
    global_logger.info(
        f"Calling check_tag_exists on repo_path: {repo_path}, tag_name: {tag_name}"
    )

    try:
        # Run the git command to list all tags
        result = subprocess.run(
            ["git", "tag"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the output and error (if any)
        global_logger.debug(
            f"Git tag command output:\n{result.stdout}\nErrors:\n{result.stderr}"
        )

        if result.returncode != 0:
            # Command execution failed
            error_message = result.stderr.strip()
            global_logger.error(
                f"Failed to list tags in repo: {repo_path}. Error: {error_message}"
            )
            return {"status": "error", "message": error_message}

        # Split the output into a list of tags
        tags = result.stdout.splitlines()
        is_tag_exists = tag_name in tags

        if is_tag_exists:
            global_logger.info(f"Tag '{tag_name}' exists in the repository.")
        else:
            global_logger.info(f"Tag '{tag_name}' does not exist in the repository.")

        return {"status": "success", "is_tag_exists": is_tag_exists}

    except Exception as e:
        global_logger.exception("An exception occurred while checking for the tag.")
        return {"status": "error", "message": str(e)}


def create_pull_request(repo_path: str, base_branch: str, pr_message: str) -> str:
    """
    Create a pull request for a Git repository.

    Args:
        repo_path (str): The path to the Git repository.
        base_branch (str): The base branch for the pull request.
        pr_message (str): The title or message of the pull request.

    Returns:
        dict: A dictionary containing the status (success or error) and the result or error message.
    """
    import subprocess

    global_logger.info(
        f"Calling create_pull_request on repo_path: {repo_path}, base_branch: {base_branch}, pr_message: {pr_message}"
    )
    global_logger.info("[Create Pull Request]")

    try:
        # Run the pull request creation command
        result = subprocess.run(
            ["cmt", "create", "--base", base_branch, "--title", pr_message],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the output and errors (if any)
        if result:
            global_logger.debug(
                f"Create PR command output:\n{result.stdout}\nErrors:\n{result.stderr}"
            )

        if result.returncode != 0:
            # Command execution failed
            error_message = result.stderr.strip()
            global_logger.error(
                f"Failed to create pull request. Error: {error_message}"
            )
            return None

        # Extract PR details from the output
        pr_links = extract_pr_list(result.stdout)

        if not pr_links:
            global_logger.warning("No pull request link found in the command output.")
            return None

        # Log and return the first PR link
        pr_link = pr_links[0]
        global_logger.info(f"Pull request created successfully: {pr_link}")
        return pr_link

    except Exception as e:
        global_logger.exception(
            "An exception occurred while creating the pull request."
        )
        return None


def get_last_modified_time(repo_path: str, relative_file_path: str) -> str:
    """
    Get the last modified time of a file in a Git repository.

    Args:
        repo_path (str): The path to the Git repository.
        relative_file_path (str): The relative path to the file within the repository.

    Returns:
        dict: A dictionary containing the status (success or error) and the result (last modified date or error message).
    """
    import subprocess

    global_logger.info(
        f"Calling get_last_modified_time on repo_path: {repo_path}, file: {relative_file_path}"
    )

    try:
        # Run the git command to get the last modified time of the file
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", "--", relative_file_path],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the output and errors (if any)
        if result:
            global_logger.debug(
                f"Git log command output:\n{result.stdout}\nErrors:\n{result.stderr}"
            )

        if result.returncode != 0:
            # Command execution failed
            error_message = result.stderr.strip()
            global_logger.warning(
                f"Failed to get last modified time for file: {relative_file_path}. Error: {error_message}"
            )
            return None

        # Process the output to get the last modified time
        last_modified_time = result.stdout.strip()

        if not last_modified_time:
            global_logger.warning(
                f"No modification history found for file: {relative_file_path}"
            )
            return None

        # Convert to desired format using mtime utilities
        last_modified_datetime = mtime.convert_str_to_datetime(
            last_modified_time, mtime.FORMAT_GIT
        )
        last_modified_date_str = mtime.convert_datetime_to_str(
            last_modified_datetime, mtime.FORMAT_DATE_YEAR_FIRST
        )

        global_logger.info(
            f"Last modified time for file '{relative_file_path}': {last_modified_date_str}"
        )
        return last_modified_date_str

    except Exception as e:
        global_logger.warning("An exception occurred while getting last modified time.")
        return None


def check_commit_diff(
    repo_path: str, old_commit: str, new_commit: str, file_path: str = None
) -> bool:
    global_logger.info(
        f"Calling check_commit_diff on repo_path: {repo_path} old_commit: {old_commit} new_commit: {new_commit} file_path: {file_path}"
    )
    global_logger.info("[Check Commit Diff]")

    """
    Check if there are any file differences between two Git commits.

    :param commit1: The SHA of the first commit
    :param commit2: The SHA of the second commit
    :return: True if there are differences, False otherwise
    """
    try:
        commands = ["git", "diff", "--name-only", old_commit, new_commit]
        if file_path:
            commands.append("--")
            commands.append(file_path)

        # Run the git diff command between the two commits
        result = mterminal.subprocess.run(
            commands,
            stdout=mterminal.subprocess.PIPE,
            stderr=mterminal.subprocess.PIPE,
            text=True,
            cwd=repo_path,
        )

        # Check if there are any differences
        if result.returncode == 0:
            if result.stdout.strip():
                # If the output is not empty, there are differences
                global_logger.debug(
                    f"Files changed between {old_commit} and {new_commit}:"
                )
                global_logger.debug(result.stdout)
                return True
            else:
                # No differences
                global_logger.debug(
                    f"No differences between {old_commit} and {new_commit}."
                )
                return False
        else:
            # Handle errors (e.g., invalid commit SHAs)
            global_logger.error(f"Error: {result.stderr}")
            return False

    except Exception as e:
        global_logger.error(f"An exception occurred: {e}")
        return False


def get_git_status_files(repo_path):
    """
    Get the list of unique folders containing files listed in `git status`.

    Args:
        repo_path (str): The path to the git repository.

    Returns:
        set: A set of unique folder paths containing the modified, untracked, or staged files.
    """
    try:
        # Run 'git status --porcelain' to get concise status output
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise global_logger.error(f"Git command failed: {result.stderr.strip()}")

        # Parse the output to extract file paths
        file_paths = []
        for line in result.stdout.splitlines():
            # Status lines start with a two-character code (e.g., " M", "??")
            if len(line) > 3:
                file_path = line[3:].strip()
                file_paths.append(file_path)
        return file_paths

    except Exception as e:
        global_logger.error(f"Error: {e}")
        return set()


# --------------------------------------- Workflow -------------------------------------


def workflow_set_up_latest_remote_node(repo_path: str, branch_name: str) -> bool:
    global_logger.info(
        f"Calling workflow_set_up_latest_remote_node on repo_path: {repo_path} branch_name: {branch_name}"
    )
    # Remove files and paths that are not staged
    execution_result = remove_untracked_files(repo_path)
    # Reset to the last commit node to avoid conflicts
    execution_result = reset_node_local(repo_path) and execution_result
    # Pull the latest code to ensure the target branch is synced from the remote
    execution_result = update_repo(repo_path) and execution_result
    # Switch to the target branch
    execution_result = (
        checkout_to_target_branch(repo_path, branch_name) and execution_result
    )
    # Ensure the repository is at the latest version
    execution_result = reset_node_remote(repo_path, branch_name) and execution_result
    # Confirm the current latest node (manual step)
    execution_result = show_latest_node(repo_path) and execution_result
    global_logger.info(
        "Worflow execution result: " + "True" if execution_result else "False"
    )
    return execution_result


def workflow_submit_gerrit(repo_path: str, branch_name: str, txt_name: str) -> str:
    global_logger.info(
        f"Calling workflow_submit_gerrit on repo_path: {repo_path} branch_name: {branch_name} txt_name: {txt_name}"
    )
    # Add all files to the staging area
    add_all_files(repo_path)
    # Commit as a node
    commit_by_txt(repo_path, txt_name)
    # Convert to refs branch name
    refs_branch = __get_refs_branch(branch_name)
    # Push to the target branch
    results = push_to_branch_dict(repo_path, refs_branch)
    execution_result = results["status"] == "success"
    global_logger.info(
        "Worflow execution result: " + "True" if execution_result else "False"
    )
    if execution_result:
        gerrit_link = results["web_links"][0]
        return gerrit_link
    else:
        return None


def workflow_is_commit_the_same(
    repo_path: str, older_sha: str, newer_sha: str, file_path: str = None
) -> bool:
    global_logger.info(
        f"Calling workflow_is_commit_the_same on repo_path: {repo_path} older_sha: {older_sha} newer_sha: {newer_sha} file_path: {file_path}"
    )
    update_repo(repo_path)
    return check_commit_diff(repo_path, older_sha, newer_sha, file_path)
