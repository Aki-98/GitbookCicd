from mstr import ENCODE

import os

from logging import Logger
from send2trash import send2trash
from shutil import rmtree

# ----------------------------- File Read/Write -----------------------------


def write_data_to_file(logger: Logger, file_all_path: str, data: str):
    """
    Write data to a file, overwriting existing content.

    :param logger: Logger for logging messages.
    :param file_all_path: Full path of the file to write.
    :param data: Data to write to the file.
    """
    logger.debug(f"[write_data_to_file] Start writing data to {file_all_path}")
    try:
        file_parent_path = os.path.dirname(file_all_path)
        if file_parent_path and not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path)
            logger.info(f"Path created: {file_parent_path}")
        with open(file_all_path, "w", encoding=ENCODE) as file:
            file.write(str(data))
        logger.debug(
            f"[write_data_to_file] Data written successfully to {file_all_path}"
        )
    except Exception as e:
        logger.error(f"[write_data_to_file] Error: {e}")


def append_data_to_file(logger: Logger, file_all_path: str, data: str):
    """
    Append data to a file without overwriting existing content.

    :param logger: Logger for logging messages.
    :param file_all_path: Full path of the file to append data to.
    :param data: Data to append to the file.
    """
    logger.debug(f"[append_data_to_file] Start appending data to {file_all_path}")
    try:
        file_parent_path = os.path.dirname(file_all_path)
        if not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path)
            logger.info(f"Path created: {file_parent_path}")
        with open(file_all_path, "a", encoding=ENCODE) as file:
            file.write(str(data))
        logger.debug(
            f"[append_data_to_file] Data appended successfully to {file_all_path}"
        )
    except Exception as e:
        logger.error(f"[append_data_to_file] Error: {e}")


def read_data_from_file(logger: Logger, file_all_path: str) -> str:
    """
    Read data from a file.

    :param logger: Logger for logging messages.
    :param file_all_path: Full path of the file to read from.
    :return: Data read from the file.
    """
    logger.debug(f"[read_data_from_file] Start reading data from {file_all_path}")
    try:
        with open(file_all_path, "r", encoding=ENCODE) as file:
            data = file.read()
        logger.debug(
            f"[read_data_from_file] Data read successfully from {file_all_path}"
        )
        return data
    except Exception as e:
        logger.error(f"[read_data_from_file] Error: {e}")


# ----------------------------- File Search -----------------------------


def find_files(
    logger: Logger, file_path: str = "", file_name: str = ".apk", filter: str = ""
) -> list:
    """
    Search for files by keyword, file format, or specific file name.

    :param logger: Logger for logging messages.
    :param file_path: Path to search within.
    :param file_name: File name or extension to search for.
    :param filter: Keyword to filter files.
    :return: List of found file paths.
    """
    logger.debug(f"[find_files] Start searching files in {file_path}")
    try:
        if filter:
            logger.debug(f"[find_files] Searching files containing '{filter}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if filter in file:
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        logger.debug(f"[find_files] Found: {found_path}")
            return found_files

        elif file_name.startswith("."):
            logger.debug(f"[find_files] Searching files with extension '{file_name}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file.endswith(file_name):
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        logger.debug(f"[find_files] Found: {found_path}")
            return found_files

        else:
            logger.debug(f"[find_files] Searching for file '{file_name}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file == file_name:
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        logger.debug(f"[find_files] Found: {found_path}")
            return found_files
    except Exception as e:
        logger.error(f"[find_files] Error: {e}")
        return []


def find_files_nc(
    logger: Logger, file_path: str = "", file_name: str = ".apk", filter: str = ""
) -> list:
    """
    Search for files in a given directory based on a keyword, file format, or specific file name.

    :param logger: Logger instance for logging.
    :param file_path: Directory path where the search is performed. Defaults to the current directory.
    :param file_name: File extension or specific file name to search for. Defaults to '.apk'.
    :param filter: A keyword to filter files by name.
    :return: A list of file paths that match the search criteria.
    """
    logger.debug(
        f"[find_files_nc] Starting search with parameters: file_path='{file_path}', file_name='{file_name}', filter='{filter}'"
    )
    try:
        # Ensure the file path exists
        if not os.path.exists(file_path):
            logger.warning(f"Provided path does not exist: {file_path}")
            return []

        # Search for files by keyword
        if filter:
            logger.debug(
                f"Searching for files containing keyword '{filter}' in '{file_path}'"
            )
            found_files = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if filter in file:
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    logger.debug(f"Found file: {found_path}")
            logger.debug(
                f"Total files found with keyword '{filter}': {len(found_files)}"
            )
            return found_files

        # Search for files by format
        elif file_name.startswith("."):
            logger.debug(
                f"Searching for files with format '{file_name}' in '{file_path}'"
            )
            found_files = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file.endswith(file_name):
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    logger.debug(f"Found file: {found_path}")
            logger.debug(
                f"Total files found with format '{file_name}': {len(found_files)}"
            )
            return found_files

        # Search for a specific file
        else:
            logger.debug(f"Searching for file named '{file_name}' in '{file_path}'")
            found_path_list = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file == file_name:
                    found_path = os.path.join(file_path, file)
                    logger.debug(f"Found file: {found_path}")
                    found_path_list.append(found_path)
            logger.debug(
                f"Total files found with name '{file_name}': {len(found_path_list)}"
            )
            return found_path_list

    except Exception as e:
        logger.error(f"[find_files_nc] An error occurred during file search: {e}")
        return []
    finally:
        logger.debug(f"[find_files_nc] Search completed for path '{file_path}'")


def find_files_nc_without_extension(
    logger: Logger, folder_path: str, *without_file_extension_list
) -> list:
    """
    Find files in a folder that do not belong to specified file extensions.

    :param logger: Logger instance for logging.
    :param folder_path: Path to the folder.
    :param without_file_extension_list: List of file extensions to exclude.
    :return: List of files that do not have the specified extensions.
    """
    logger.debug(f"Starting search in folder: {folder_path}")
    logger.debug(f"Excluding files with extensions: {without_file_extension_list}")

    # Validate the folder path
    if not os.path.isdir(folder_path):
        logger.error(f"The folder path '{folder_path}' is not a valid directory.")
        raise ValueError(f"The folder path '{folder_path}' is not a valid directory.")

    # Convert the extensions to lowercase and validate input
    excluded_extensions = tuple(
        ext.lower() for ext in without_file_extension_list if isinstance(ext, str)
    )
    logger.debug(f"Converted excluded extensions to lowercase: {excluded_extensions}")

    try:
        # Filter files in the folder
        files = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))  # Include only files
            and not f.lower().endswith(
                excluded_extensions
            )  # Exclude specified extensions
        ]
        logger.info(f"Found {len(files)} files not matching the excluded extensions.")
        for file in files:
            logger.debug(f"File included: {file}")

        return files
    except Exception as e:
        logger.error(f"An error occurred while searching files: {e}")


# ----------------------------- Delete Files -----------------------------


def delete_files(logger: Logger, file_path: str = "", file_name_or_format: str = ""):
    """
    Delete all files, files of a specific format, or a specific file in a directory.

    :param logger: Logger for logging messages.
    :param file_path: Path to the directory.
    :param file_name_or_format: Specific file name or format to delete.
    """
    logger.debug(f"[delete_files] Start deleting in {file_path}")
    try:
        if file_name_or_format == "":
            logger.debug(f"[delete_files] Deleting all files in {file_path}")
            rmtree(file_path)
        elif file_name_or_format.startswith("."):
            logger.debug(
                f"[delete_files] Deleting files with extension '{file_name_or_format}'"
            )
            for file in find_files(logger, file_path, file_name=file_name_or_format):
                os.remove(file)
        else:
            logger.debug(
                f"[delete_files] Deleting specific file '{file_name_or_format}'"
            )
            os.remove(join_file_path(file_path, file_name_or_format))
        logger.info(f"[delete_files] Deletion successful")
    except Exception as e:
        logger.error(f"[delete_files] Error: {e}")


def move_to_recycle_bin(logger: Logger, file_path: str):
    """
    Move file or folder to the recycle bin.
    :param file_path: The path of the file or folder.
    """
    try:
        send2trash(file_path)
        logger.debug(f"Moved to recycle bin: {file_path}")
    except Exception as e:
        logger.error(f"Error: {e}")


def remove_empty_folders(logger: Logger, directory: str):
    """
    Recursively delete all empty folders in the specified directory.

    :param directory: The path of the directory to clean.
    """
    # Traverse all files and subdirectories in the directory
    for foldername, subfolders, filenames in os.walk(directory, topdown=False):
        # Traverse all subdirectories
        for subfolder in subfolders:
            folder_path = os.path.join(foldername, subfolder)
            # If the folder is empty, delete it
            if not os.listdir(folder_path):  # Folder is empty
                os.rmdir(folder_path)
                logger.debug(f"Deleted empty folder: {folder_path}")


# ----------------------------- Tools Method -----------------------------


def get_filename_from_pathall(logger: Logger, file_path_all: str) -> str:
    """
    Extract the file name from a full file path.

    :param logger: Logger instance for logging.
    :param file_path_all: The full file path.
    :return: The file name extracted from the path.
    """
    logger.debug(f"Extracting file name from full path: {file_path_all}")
    filename = os.path.basename(file_path_all)
    logger.debug(f"Extracted file name: {filename}")
    return filename


def resolve_relative_path(logger: Logger, path: str) -> str:
    """
    Resolve a relative path containing `..` components to an absolute path.

    :param logger: Logger instance for logging.
    :param path: The input path containing `..` components.
    :return: The resolved absolute path.
    """
    logger.debug(f"Resolving relative path: {path}")
    resolved_path = os.path.normpath(path)
    logger.debug(f"Resolved path: {resolved_path}")
    return resolved_path


def get_filepath_from_pathall(logger: Logger, file_path_all: str) -> str:
    """
    Extract the directory path from a full file path.

    :param logger: Logger instance for logging.
    :param file_path_all: The full file path.
    :return: The directory path extracted from the full path.
    """
    logger.debug(f"Extracting directory path from full path: {file_path_all}")
    drive, path_without_drive = os.path.splitdrive(file_path_all)
    directory_path = os.path.dirname(path_without_drive)
    full_path = os.path.join(drive, directory_path)
    logger.debug(f"Extracted directory path: {full_path}")
    return full_path


def join_file_path(logger: Logger, *args: str) -> str:
    """
    Join multiple path components into a single file path.

    :param logger: Logger instance for logging.
    :param args: Path components to join.
    :return: The joined file path.
    """
    logger.debug(f"Joining path components: {args}")
    if args[0] == "":
        joined_path = os.path.join(*args[1:])
    else:
        joined_path = os.path.join(*args)
    normalized_path = joined_path.replace("/", "\\")
    logger.debug(f"Joined and normalized path: {normalized_path}")
    return normalized_path


def get_basename(logger: Logger, file_path: str) -> str:
    """
    Extract the base name (file name without extension) from a file path.

    :param logger: Logger instance for logging.
    :param file_path: The full file path.
    :return: The base name of the file.
    """
    logger.debug(f"Extracting base name from file path: {file_path}")
    basename, _ = os.path.splitext(os.path.basename(file_path))
    logger.debug(f"Extracted base name: {basename}")
    return basename


def get_extension(logger: Logger, file_path: str) -> str:
    """
    Extract the file extension from a file path.

    :param logger: Logger instance for logging.
    :param file_path: The full file path.
    :return: The file extension.
    """
    logger.debug(f"Extracting file extension from file path: {file_path}")
    _, extension = os.path.splitext(file_path)
    logger.debug(f"Extracted extension: {extension}")
    return extension


def rollback_path(logger: Logger, path: str, levels: int) -> str:
    """
    Roll back a specified path by a given number of levels.

    :param logger: Logger instance for logging.
    :param path: The original file or directory path.
    :param levels: Number of levels to roll back (default is 2).
    :return: The rolled-back path.
    """
    logger.debug(f"Rolling back path: {path} by {levels} levels")
    if levels < 0:
        logger.error("Levels must be a non-negative integer.")
        raise ValueError("Levels must be a non-negative integer.")
    original_path = path
    for _ in range(levels):
        path = os.path.dirname(path)
    logger.debug(f"Rolled back path from {original_path} to {path}")
    return path


# ----------------------------- File Size -----------------------------


def get_file_size_mb(logger: Logger, file_path: str) -> float:
    """
    Get the size of a file in megabytes (MB).

    :param logger: Logger instance for debugging and error logging.
    :param file_path: The path of the file to check size.
    :return: File size in MB.
    """
    try:
        logger.debug(f"Calculating file size for: {file_path}")
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        logger.debug(f"File size for {file_path}: {file_size_mb:.2f} MB")
        return file_size_mb
    except Exception as e:
        logger.error(f"Error calculating file size: {e}")
        return 0.0
