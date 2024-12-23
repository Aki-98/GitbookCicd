from logging import Logger
import subprocess


def get_git_status_files(logger: Logger, repo_path: str):
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
            raise logger.error(f"Git command failed: {result.stderr.strip()}")

        # Parse the output to extract file paths
        file_paths = []
        for line in result.stdout.splitlines():
            # Status lines start with a two-character code (e.g., " M", "??")
            if len(line) > 3:
                file_path = line[3:].strip()
                file_paths.append(file_path)
        return file_paths

    except Exception as e:
        logger.error(f"Error: {e}")
        return []
