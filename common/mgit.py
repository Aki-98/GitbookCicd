import subprocess
import codecs
import re


def get_git_status_files(repo_path: str):
    """
    Get the list of unique folders containing files listed in `git status`.

    Args:
        repo_path (str): The path to the git repository.

    Returns:
        set: A set of unique folder paths containing the modified, untracked, or staged files.
    """
    from common.mlogger import global_logger

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

        output = result.stdout
        # Decode octal escape characters in the path
        decoded_output = codecs.decode(output, "unicode_escape")
        # Check if the path contains incorrectly decoded UTF-8 characters (e.g., é¡¹ç, etc.)
        try:
            decoded_output = decoded_output.encode("latin1").decode("utf-8")
        except Exception:
            pass
        changed_file_pattern = r"(?:D|M|A|\?\?)\s+([^\s]+)"
        changed_file_matches = re.findall(changed_file_pattern, decoded_output)
        return changed_file_matches

    except Exception as e:
        global_logger.error(f"Error: {e}")
        return []
