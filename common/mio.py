from mstr import ENCODE

import os

import send2trash
import shutil

# ----------------------------- File Read/Write -----------------------------


def write_data_to_file(file_all_path: str, data: str):
    """
    Write data to a file, overwriting existing content.

    :param global_logger: global_logger for logging messages.
    :param file_all_path: Full path of the file to write.
    :param data: Data to write to the file.
    """

    from common.mlogger import global_logger

    global_logger.debug(f"[write_data_to_file] Start writing data to {file_all_path}")
    try:
        file_parent_path = os.path.dirname(file_all_path)
        if file_parent_path and not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path)
            global_logger.info(f"Path created: {file_parent_path}")
        with open(file_all_path, "w", encoding=ENCODE) as file:
            file.write(str(data))
        global_logger.debug(
            f"[write_data_to_file] Data written successfully to {file_all_path}"
        )
    except Exception as e:
        global_logger.error(f"[write_data_to_file] Error: {e}")


def append_data_to_file(file_all_path: str, data: str):
    """
    Append data to a file without overwriting existing content.

    :param global_logger: global_logger for logging messages.
    :param file_all_path: Full path of the file to append data to.
    :param data: Data to append to the file.
    """
    from common.mlogger import global_logger

    global_logger.debug(
        f"[append_data_to_file] Start appending data to {file_all_path}"
    )
    try:
        file_parent_path = os.path.dirname(file_all_path)
        if not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path)
            global_logger.info(f"Path created: {file_parent_path}")
        with open(file_all_path, "a", encoding=ENCODE) as file:
            file.write(str(data))
        global_logger.debug(
            f"[append_data_to_file] Data appended successfully to {file_all_path}"
        )
    except Exception as e:
        global_logger.error(f"[append_data_to_file] Error: {e}")


def read_data_from_file(file_all_path: str) -> str:
    """
    Read data from a file.

    :param global_logger: global_logger for logging messages.
    :param file_all_path: Full path of the file to read from.
    :return: Data read from the file.
    """
    from common.mlogger import global_logger

    global_logger.debug(
        f"[read_data_from_file] Start reading data from {file_all_path}"
    )
    try:
        with open(file_all_path, "r", encoding=ENCODE) as file:
            data = file.read()
        global_logger.debug(
            f"[read_data_from_file] Data read successfully from {file_all_path}"
        )
        return data
    except Exception as e:
        global_logger.error(f"[read_data_from_file] Error: {e}")


# ----------------------------- File Search -----------------------------


def find_files(file_path: str = "", file_name: str = ".apk", filter: str = "") -> list:
    """
    Search for files by keyword, file format, or specific file name.

    :param global_logger: global_logger for logging messages.
    :param file_path: Path to search within.
    :param file_name: File name or extension to search for.
    :param filter: Keyword to filter files.
    :return: List of found file paths.
    """
    from common.mlogger import global_logger

    global_logger.debug(f"[find_files] Start searching files in {file_path}")
    try:
        if filter:
            global_logger.debug(f"[find_files] Searching files containing '{filter}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if filter in file:
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        # global_logger.debug(f"[find_files] Found: {found_path}")
            return found_files

        elif file_name.startswith("."):
            global_logger.debug(
                f"[find_files] Searching files with extension '{file_name}'"
            )
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file.endswith(file_name):
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        # global_logger.debug(f"[find_files] Found: {found_path}")
            return found_files

        else:
            global_logger.debug(f"[find_files] Searching for file '{file_name}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file == file_name:
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        # global_logger.debug(f"[find_files] Found: {found_path}")
            return found_files
    except Exception as e:
        global_logger.error(f"[find_files] Error: {e}")
        return []


def find_files_nc(
    file_path: str = "", file_name: str = ".apk", filter: str = ""
) -> list:
    """
    Search for files in a given directory based on a keyword, file format, or specific file name.

    :param global_logger: global_logger instance for logging.
    :param file_path: Directory path where the search is performed. Defaults to the current directory.
    :param file_name: File extension or specific file name to search for. Defaults to '.apk'.
    :param filter: A keyword to filter files by name.
    :return: A list of file paths that match the search criteria.
    """
    from common.mlogger import global_logger

    global_logger.debug(
        f"[find_files_nc] Starting search with parameters: file_path='{file_path}', file_name='{file_name}', filter='{filter}'"
    )
    try:
        # Ensure the file path exists
        if not os.path.exists(file_path):
            global_logger.warning(f"Provided path does not exist: {file_path}")
            return []

        # Search for files by keyword
        if filter:
            global_logger.debug(
                f"Searching for files containing keyword '{filter}' in '{file_path}'"
            )
            found_files = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if filter in file:
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    global_logger.debug(f"Found file: {found_path}")
            global_logger.debug(
                f"Total files found with keyword '{filter}': {len(found_files)}"
            )
            return found_files

        # Search for files by format
        elif file_name.startswith("."):
            global_logger.debug(
                f"Searching for files with format '{file_name}' in '{file_path}'"
            )
            found_files = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file.endswith(file_name):
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    global_logger.debug(f"Found file: {found_path}")
            global_logger.debug(
                f"Total files found with format '{file_name}': {len(found_files)}"
            )
            return found_files

        # Search for a specific file
        else:
            global_logger.debug(
                f"Searching for file named '{file_name}' in '{file_path}'"
            )
            found_path_list = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file == file_name:
                    found_path = os.path.join(file_path, file)
                    global_logger.debug(f"Found file: {found_path}")
                    found_path_list.append(found_path)
            global_logger.debug(
                f"Total files found with name '{file_name}': {len(found_path_list)}"
            )
            return found_path_list

    except Exception as e:
        global_logger.error(
            f"[find_files_nc] An error occurred during file search: {e}"
        )
        return []
    finally:
        global_logger.debug(f"[find_files_nc] Search completed for path '{file_path}'")


def find_files_nc_without_extension(
    folder_path: str, *without_file_extension_list
) -> list:
    """
    Find files in a folder that do not belong to specified file extensions.

    :param folder_path: Path to the folder.
    :param without_file_extension_list: List of file extensions to exclude.
    :return: List of files that do not have the specified extensions.
    """
    from common.mlogger import global_logger

    global_logger.debug(f"Starting search in folder: {folder_path}")
    global_logger.debug(
        f"Excluding files with extensions: {without_file_extension_list}"
    )

    # Validate the folder path
    if not os.path.isdir(folder_path):
        global_logger.error(
            f"The folder path '{folder_path}' is not a valid directory."
        )

    # Convert the extensions to lowercase and validate input
    excluded_extensions = tuple(
        ext.lower() for ext in without_file_extension_list if isinstance(ext, str)
    )
    global_logger.debug(
        f"Converted excluded extensions to lowercase: {excluded_extensions}"
    )

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
        global_logger.info(
            f"Found {len(files)} files not matching the excluded extensions."
        )
        for file in files:
            global_logger.debug(f"File included: {file}")

        return files
    except Exception as e:
        global_logger.error(f"An error occurred while searching files: {e}")


# ----------------------------- Delete Files -----------------------------


def delete_files(file_path: str = "", file_name_or_format: str = ""):
    """
    Delete all files, files of a specific format, or a specific file in a directory.

    :param global_logger: global_logger for logging messages.
    :param file_path: Path to the directory.
    :param file_name_or_format: Specific file name or format to delete.
    """
    from common.mlogger import global_logger

    global_logger.debug(f"[delete_files] Start deleting in {file_path}")
    try:
        if file_name_or_format == "":
            global_logger.debug(f"[delete_files] Deleting all files in {file_path}")
            shutil.rmtree(file_path)
            return
        elif file_name_or_format.startswith("."):
            global_logger.debug(
                f"[delete_files] Deleting files with extension: '{file_name_or_format}'"
            )
        else:
            global_logger.debug(
                f"[delete_files] Deleting files with name: '{file_name_or_format}'"
            )
        for file in find_files(file_path, file_name=file_name_or_format):
            os.remove(file)
        global_logger.info(f"[delete_files] Deletion successful")
    except Exception as e:
        global_logger.error(f"[delete_files] Error: {e}")


def move_to_recycle_bin(file_path: str):
    """
    Move file or folder to the recycle bin.
    :param file_path: The path of the file or folder.
    """
    from common.mlogger import global_logger

    try:
        send2trash.send2trash(file_path)
        global_logger.debug(f"Moved to recycle bin: {file_path}")
    except Exception as e:
        global_logger.error(f"Error: {e}")


def remove_empty_folders(directory: str):
    """
    Recursively delete all empty folders in the specified directory.

    :param directory: The path of the directory to clean.
    """
    from common.mlogger import global_logger

    # Traverse all files and subdirectories in the directory
    for foldername, subfolders, filenames in os.walk(directory, topdown=False):
        # Traverse all subdirectories
        for subfolder in subfolders:
            folder_path = os.path.join(foldername, subfolder)
            # If the folder is empty, delete it
            if not os.listdir(folder_path):  # Folder is empty
                os.rmdir(folder_path)
                global_logger.debug(f"Deleted empty folder: {folder_path}")


# ----------------------------- File Copy -----------------------------


def copy_files(
    from_folder_path: str = "/",
    from_file_name_or_format: str = "",
    to_folder_path: str = "/",
    to_file_name: str = "",
):
    """Copy all files/copy all files of a specific format in a file tree/copy a single file."""
    from common.mlogger import global_logger

    try:
        # If no file is specified, copy all files
        if "" == from_file_name_or_format:
            global_logger.debug(
                f"copy all file in folder {from_folder_path} to folder {to_folder_path}"
            )
            if not os.path.exists(to_folder_path):
                global_logger.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                os.makedirs(to_folder_path)
                global_logger.info(f"succeed in makedirs!")
            shutil.copytree(from_folder_path, to_folder_path)
        # If a file format is passed, copy files of that format
        elif from_file_name_or_format.startswith("."):
            global_logger.debug(
                f"copy file of format {from_file_name_or_format} in folder {from_folder_path} to folder {to_folder_path}"
            )
            found_files = find_files(from_folder_path, from_file_name_or_format)
            if not found_files:
                global_logger.warning(
                    f"file in format {from_file_name_or_format} not found"
                )
                return
            if not os.path.exists(to_folder_path):
                global_logger.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                os.makedirs(to_folder_path)
                global_logger.info(f"succeed in makedirs!")
            for file in found_files:
                shutil.copy(file, to_folder_path)
        # Copy a specific file
        else:
            if "" == to_file_name:
                to_file_name = from_file_name_or_format
            global_logger.debug(
                f"copy file of name {from_file_name_or_format} in folder {from_folder_path} to folder {to_folder_path}, and renamed as {to_file_name}"
            )
            if not os.path.exists(to_folder_path):
                global_logger.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                os.makedirs(to_folder_path)
                global_logger.info(f"succeed in makedirs!")
            shutil.copy(
                join_file_path(from_folder_path, from_file_name_or_format),
                join_file_path(to_folder_path, to_file_name),
            )
        global_logger.info(f"succeed in copy files!")
    except Exception as e:
        global_logger.error(f"error: {e}")


# ----------------------------- Tools Method -----------------------------


def get_filename_from_pathall(file_path_all: str) -> str:
    """
    Extract the file name from a full file path.

    :param file_path_all: The full file path.
    :return: The file name extracted from the path.
    """
    filename = os.path.basename(file_path_all)
    return filename


def resolve_relative_path(path: str) -> str:
    """
    Resolve a relative path containing `..` components to an absolute path.

    :param path: The input path containing `..` components.
    :return: The resolved absolute path.
    """
    resolved_path = os.path.normpath(path)
    return resolved_path


def get_filepath_from_pathall(file_path_all: str) -> str:
    """
    Extract the directory path from a full file path.

    :param file_path_all: The full file path.
    :return: The directory path extracted from the full path.
    """
    drive, path_without_drive = os.path.splitdrive(file_path_all)
    directory_path = os.path.dirname(path_without_drive)
    full_path = os.path.join(drive, directory_path)
    return full_path


def join_file_path(*args: str) -> str:
    """
    Join multiple path components into a single file path.

    :param args: Path components to join.
    :return: The joined file path.
    """
    if args[0] == "":
        joined_path = os.path.join(*args[1:])
    else:
        joined_path = os.path.join(*args)
    normalized_path = joined_path.replace("/", "\\")
    return normalized_path


def get_basename(file_path: str) -> str:
    """
    Extract the base name (file name without extension) from a file path.

    :param file_path: The full file path.
    :return: The base name of the file.
    """
    basename, _ = os.path.splitext(os.path.basename(file_path))
    return basename


def get_extension(file_path: str) -> str:
    """
    Extract the file extension from a file path.

    :param file_path: The full file path.
    :return: The file extension.
    """
    _, extension = os.path.splitext(file_path)
    return extension


def rollback_path(path: str, levels: int) -> str:
    """
    Roll back a specified path by a given number of levels.

    :param path: The original file or directory path.
    :param levels: Number of levels to roll back (default is 2).
    :return: The rolled-back path.
    """

    if levels < 0:
        raise ValueError("Levels must be a non-negative integer.")
    for _ in range(levels):
        path = os.path.dirname(path)
    return path


# ----------------------------- File Size -----------------------------


def get_file_size_mb(file_path: str) -> float:
    """
    Get the size of a file in megabytes (MB).

    :param global_logger: global_logger instance for debugging and error logging.
    :param file_path: The path of the file to check size.
    :return: File size in MB.
    """
    from common.mlogger import global_logger

    try:
        global_logger.debug(f"Calculating file size for: {file_path}")
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        global_logger.debug(f"File size for {file_path}: {file_size_mb:.2f} MB")
        return file_size_mb
    except Exception as e:
        global_logger.error(f"Error calculating file size: {e}")
        return 0.0
