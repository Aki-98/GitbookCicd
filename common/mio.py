from zipfile import ZIP_DEFLATED
from mstr import ENCODE

from zipfile import ZipFile
from send2trash import send2trash

from mlogger import global_logger

from os import path, makedirs, walk, remove
from shutil import rmtree, copy, copytree
from json import load, dumps

import mprint
import minput

# ----------------------------- File Read/Write -----------------------------


def write_data_to_file(file_all_path: str, data: str):
    try:
        file_parent_path = path.dirname(file_all_path)
        # Check if the directory exists
        # TODO: Solve the issue where only the file name is passed, and it's written to the current path, needs verification
        if file_parent_path:
            if not path.exists(file_parent_path):
                # If the directory does not exist, create the path using os.makedirs
                makedirs(file_parent_path)
                global_logger.info(f"path has been created: {file_parent_path}")
            # Open the file and write data in write mode, clearing previous content
        with open(file_all_path, "w", encoding=ENCODE) as file:
            file.write(str(data))
        # global_logger.debug(f"[write_data_to_file] Data successfully written to file: {data}")
    except Exception as e:
        global_logger.error(f"error: {e}")


def append_data_to_file(file_all_path: str, data: str):
    try:
        file_parent_path = path.dirname(file_all_path)
        # Check if the directory exists
        if not path.exists(file_parent_path):
            # If the directory does not exist, create the path using os.makedirs
            makedirs(file_parent_path)
            global_logger.info(f"path has been created: {file_parent_path}")
        # Open the file in append mode, writing data without clearing previous content
        with open(file_all_path, "a", encoding=ENCODE) as file:
            file.write(str(data))
        # global_logger.debug(f"[append_data_to_file] Data successfully appended to file: {data}")
    except Exception as e:
        global_logger.error(f"error: {e}")


def read_data_from_file(file_all_path: str) -> str:
    try:
        # Open the file in read mode to read the data
        with open(file_all_path, "r", encoding=ENCODE) as file:
            data = file.read()
        # global_logger.debug(f"[read_data_from_file] Successfully read data from file: {data}")
        return data
    except Exception as e:
        global_logger.error(f"error: {e}")


# ----------------------------- JSON Read/Write -----------------------------


def get_json_from_file(file_all_path: str) -> dict:
    try:
        with open(file_all_path, "r", encoding=ENCODE) as file:
            json_data = load(file)
        return json_data
    except Exception as e:
        global_logger.warning(f"error: {e}")


def write_json_to_file(file_all_path: str, json_data: str):
    try:
        json_data = dumps(json_data, indent=4, ensure_ascii=False)
        create_folder_of_file_if_not_exist(file_all_path)
        write_data_to_file(file_all_path, json_data)
    except Exception as e:
        global_logger.error(f"error: {e}")


# ----------------------------- File Search -----------------------------


def find_files(file_path: str = "", file_name: str = ".apk", filter: str = "") -> list:
    """Search for files by keyword/file format/individual file.

    Use file extension to get all files by traversing the file tree; the input file extension should start with '.', defaulting to apk files.
    If searching for a file format, returns a list; if searching for a single file, returns the file path.
    """
    try:
        # Search for files by keyword
        if filter:
            found_files = []
            global_logger.debug(
                f"find files that contains {filter} in folder {file_path}"
            )
            for root, dirs, files in walk(file_path):
                for file in files:
                    if filter in file:
                        found_path = path.join(root, file)
                        found_files.append(found_path)
                        global_logger.debug("found: " + found_path)
            return found_files
        # Search for files by format
        elif file_name.startswith("."):
            found_files = []
            global_logger.debug(f"find files of format {filter} in folder {file_path}")
            for root, dirs, files in walk(file_path):
                for file in files:
                    if file.endswith(file_name):
                        found_path = path.join(root, file)
                        found_files.append(found_path)
                        global_logger.debug("found: " + found_path)
            return found_files
        # Search for a specific file
        else:
            global_logger.debug(
                f"find files of name {file_name} in folder {file_path} (will only returned the first one found)"
            )
            found_path_list = []
            for root, dirs, files in walk(file_path):
                for file in files:
                    if file == file_name:
                        found_path = path.join(root, file)
                        global_logger.debug(f"Found file {found_path}")
                        found_path_list.append(found_path)
            return found_path_list
    except Exception as e:
        global_logger.warning(f"error: {e}")
    return []


def find_files_nc(
    file_path: str = "", file_name: str = ".apk", filter: str = ""
) -> list:
    """Search for files by keyword/file format/individual file.

    Use file extension to get all files by traversing the file tree; the input file extension should start with '.', defaulting to apk files.
    If searching for a file format, returns a list; if searching for a single file, returns the file path.
    """
    try:
        # Search for files by keyword
        if filter:
            found_files = []
            global_logger.debug(
                f"Find files that contain {filter} in folder {file_path}"
            )
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if filter in file:
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    global_logger.debug("Found: " + found_path)
            return found_files

        # Search for files by format
        elif file_name.startswith("."):
            found_files = []
            global_logger.debug(f"Find files of format {filter} in folder {file_path}")
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file.endswith(file_name):
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    global_logger.debug("Found: " + found_path)
            return found_files

        # Search for a specific file
        else:
            global_logger.debug(
                f"Find files of name {file_name} in folder {file_path} (only returns the first one found)"
            )
            found_path_list = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file == file_name:
                    found_path = os.path.join(file_path, file)
                    global_logger.debug(f"Found file {found_path}")
                    found_path_list.append(found_path)
            return found_path_list

    except Exception as e:
        global_logger.warning(f"Error: {e}")

    return []


# ----------------------------- Delete Files -----------------------------


def delete_files(file_path: str = "", file_name_or_format: str = ""):
    """Delete all files/delete all files of a specific format in a file tree/delete a single file."""
    try:
        # If no file is specified, delete all files
        if "" == file_name_or_format:
            # Recursively delete folder and its contents
            global_logger.debug(f"delete all file in folder {file_path}")
            rmtree(file_path)
        # If a file format is passed, recursively delete files of that format
        elif file_name_or_format.startswith("."):
            global_logger.debug(
                f"delete file of format {file_name_or_format} in folder {file_path}"
            )
            found_files = find_files(file_path, file_name_or_format)
            for file in found_files:
                remove(file)
        # Delete a specific file
        else:
            global_logger.debug(
                f"delete file of name {file_name_or_format} in folder {file_path}"
            )
            remove(join_file_path(file_path, file_name_or_format))
        global_logger.info(f"succeed!")
    except Exception as e:
        global_logger.error(f"error: {e}")


def move_to_recycle_bin(file_path):
    """
    Move file or folder to the recycle bin.
    :param file_path: The path of the file or folder.
    """
    try:
        send2trash(file_path)
        global_logger.debug(f"Moved to recycle bin: {file_path}")
    except Exception as e:
        global_logger.error(f"Error: {e}")


def remove_empty_folders(directory: str):
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
                global_logger.debug(f"Deleted empty folder: {folder_path}")


# ----------------------------- Copy Files -----------------------------


def copy_files(
    from_folder_path: str = "/",
    from_file_name_or_format: str = "",
    to_folder_path: str = "/",
    to_file_name: str = "",
):
    """Copy all files/copy all files of a specific format in a file tree/copy a single file."""
    try:
        # If no file is specified, copy all files
        if "" == from_file_name_or_format:
            global_logger.debug(
                f"copy all file in folder {from_folder_path} to folder {to_folder_path}"
            )
            if not path.exists(to_folder_path):
                global_logger.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                makedirs(to_folder_path)
                global_logger.info(f"succeed in makedirs!")
            copytree(from_folder_path, to_folder_path)
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
            if not path.exists(to_folder_path):
                global_logger.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                makedirs(to_folder_path)
                global_logger.info(f"succeed in makedirs!")
            for file in found_files:
                copy(file, to_folder_path)
        # Copy a specific file
        else:
            if "" == to_file_name:
                to_file_name = from_file_name_or_format
            global_logger.debug(
                f"copy file of name {from_file_name_or_format} in folder {from_folder_path} to folder {to_folder_path}, and renamed as {to_file_name}"
            )
            if not path.exists(to_folder_path):
                global_logger.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                makedirs(to_folder_path)
                global_logger.info(f"succeed in makedirs!")
            copy(
                join_file_path(from_folder_path, from_file_name_or_format),
                join_file_path(to_folder_path, to_file_name),
            )
        global_logger.info(f"succeed in copy files!")
    except Exception as e:
        global_logger.error(f"error: {e}")


def copy_folder(from_folder_path: str, to_folder_path: str):
    import shutil

    """
    Copy all files and subfolders from one folder to another, preserving the folder structure.

    :param from_folder_path: Source folder path.
    :param to_folder_path: Destination folder path.
    """
    try:
        # Check if the source folder exists
        if not os.path.exists(from_folder_path):
            raise FileNotFoundError(
                f"Source folder '{from_folder_path}' does not exist!"
            )

        # Ensure the destination folder exists
        if not os.path.exists(to_folder_path):
            os.makedirs(to_folder_path)
            global_logger.info(f"Created target folder: {to_folder_path}")

        # Traverse the source folder and its subfolders
        for root, dirs, files in os.walk(from_folder_path):
            # Copy subfolder structure
            for dir_name in dirs:
                src_dir = os.path.join(root, dir_name)
                dest_dir = os.path.join(
                    to_folder_path, os.path.relpath(src_dir, from_folder_path)
                )
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    global_logger.debug(f"Created subdirectory: {dest_dir}")

            # Copy files
            for file_name in files:
                src_file = os.path.join(root, file_name)
                dest_file = os.path.join(
                    to_folder_path, os.path.relpath(src_file, from_folder_path)
                )
                shutil.copy2(src_file, dest_file)
                global_logger.debug(f"Copied file: {src_file} to {dest_file}")

        global_logger.info(
            f"Successfully copied all files and subfolders from '{from_folder_path}' to '{to_folder_path}'."
        )

    except Exception as e:
        global_logger.error(f"Error while copying files: {e}")


def find_files_nc_without_extension(folder_path, *without_file_extension_list):
    """
    Find files in a folder that do not belong to specified file extensions.

    :param folder_path: Path to the folder.
    :param without_file_extension_list: List of file extensions to exclude.
    :return: List of files that do not have the specified extensions.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"The folder path '{folder_path}' is not a valid directory.")

    # Convert the extensions to lowercase and validate
    excluded_extensions = tuple(
        ext.lower() for ext in without_file_extension_list if isinstance(ext, str)
    )

    # Filter files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))  # Include only files
        and not f.lower().endswith(excluded_extensions)  # Exclude specified extensions
    ]
    return files


# ----------------------------- Zip Files -----------------------------


def zip_file(file_path: str, zip_path: str):
    """Compress a file using zip.
    BUG: Cannot be decompressed using 7zip
    """
    zip_file = ZipFile(zip_path, "w")
    zip_file.write(
        file_path,
        compress_type=ZIP_DEFLATED,
        arcname=get_filename_from_pathall(file_path),
    )
    zip_file.close()


# ----------------------------- Tools Method -----------------------------


def get_filename_from_pathall(file_path_all: str) -> str:
    return path.basename(file_path_all)


def resolve_relative_path(path: str) -> str:
    """
    Resolve a given path with `..` components to its absolute path.

    Args:
        path (str): The input path containing `..` components.

    Returns:
        str: The resolved absolute path.
    """
    resolved_path = os.path.normpath(path)
    return resolved_path


def get_filepath_from_pathall(file_path_all: str) -> str:
    # Split the path into drive and path components
    drive, path_without_drive = path.splitdrive(file_path_all)
    # Get the directory path
    directory_path = path.dirname(path_without_drive)
    # Return the full path including the drive
    return path.join(drive, directory_path)


def join_file_path(*args: str) -> str:
    if "" == args[0]:
        return path.join(args[1:])
    joined_path = path.join(*args)
    return joined_path.replace("/", "\\")


def join_file_path_remote(*args: str) -> str:
    joined_path = join_file_path(*args)
    return joined_path.replace("\\", "/")


def is_file_exist(path_all_file: str) -> bool:
    return path.exists(path_all_file)


def create_folder_of_file_if_not_exist(file_path_all: str):
    parent_folder = path.dirname(file_path_all)
    if not parent_folder:
        makedirs(parent_folder)


def get_basename(file_path: str) -> str:
    basename, _ = os.path.splitext(os.path.basename(file_path))
    return basename


def get_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension


def rollback_path(path, levels):
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

import os


def get_file_size_mb(file_path: str) -> float:
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    return file_size_mb


# ----------------------------- Workflow Method -----------------------------


def workflow_replace_apk(source_apk_path_all, target_apk_path, module_name):
    print(source_apk_path_all)
    global_logger.debug("Replacing release unsigned apk...")
    apk_name = get_filename_from_pathall(source_apk_path_all)
    if "release" not in apk_name.lower() or "unsigned" not in apk_name.lower():
        global_logger.warning("File name of apk not in format")
        mprint.printc_warning(
            "The app name does not meet the format, please confirm: " + apk_name
        )
        minput.exit_or_continue()
    # Copy the apk from the task directory to the submission directory
    source_apk_path = get_filepath_from_pathall(source_apk_path_all)
    copy_files(
        from_folder_path=source_apk_path,
        from_file_name_or_format=apk_name,
        to_folder_path=target_apk_path,
        to_file_name=module_name + ".apk",
    )
    minput.exit_or_continue()
