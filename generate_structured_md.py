import os

from common import mio

FILE_README = "README.md"
FILE_SUMMARY = "SUMMARY.md"
FILE_REFERS = "REFERS.md"
FILE_EXTENSION_MD = ".md"
FILE_EXTENSION_TXT = ".txt"
FILE_EXTENSION_JSON = ".json"
INDENT = "  "


def __split_path_after_keyword(path, keyword):
    parts = path.split(keyword, 1)
    if len(parts) > 1:
        splited_path = parts[1].lstrip(os.path.sep)
        return splited_path
    else:
        return None


def __create_empty_readme(folder_path):
    readme_path = os.path.join(folder_path, "README.md")

    # Check if README.md exists, create it if not
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# " + os.path.basename(folder_path).capitalize() + "\n\n")

    global_logger.info(f"Empty README.md successfully created in {folder_path}")
    return mio.join_file_path(folder_path, FILE_README)


def __txt_to_md(file_path: str):
    txt_file_list = mio.find_files(file_path=file_path, file_name=FILE_EXTENSION_TXT)
    for txt_file in txt_file_list:
        global_logger.debug(f"Found txt file: {txt_file}")
        txt_file_path = mio.get_filepath_from_pathall(txt_file)
        txt_file_name = mio.get_filename_from_pathall(txt_file)
        md_file_name = txt_file_name.replace(FILE_EXTENSION_TXT, FILE_EXTENSION_MD)
        mio.copy_files(
            from_folder_path=txt_file_path,
            from_file_name_or_format=txt_file_name,
            to_folder_path=txt_file_path,
            to_file_name=md_file_name,
        )
        global_logger.debug(f"Converted to md file: {md_file_name}")
        mio.delete_files(
            global_logger, file_path=txt_file_path, file_name_or_format=txt_file_name
        )
        global_logger.info("Deleted txt file successfully")


def __clean_readme_refers(file_path: str):
    global_logger.debug(f"Delete all {FILE_README} and {FILE_REFERS}...")
    mio.delete_files(file_path, FILE_README)
    mio.delete_files(file_path, FILE_REFERS)


def __generate_readme_refers_summary(root_dir, current_dir, indent):
    """
    Recursively generate the directory structure of .md files in the specified folder.

    Parameters:
    - folder_path: Path to the specified folder
    - indent: Indentation string

    Returns:
    - md_structure: Generated directory structure of .md files
    """
    summary_structure = ""

    # Iterate through all files and subfolders in the directory
    for item in os.listdir(current_dir):
        item_path = mio.join_file_path(current_dir, item)
        global_logger.debug(f"Item: {item}")
        # If it's a folder and not a folder containing imgs, files, .git, or node_modules, recursively generate the subdirectory structure
        if (
            "_imgs" not in item
            and "_files" not in item
            and ".git" != item
            and "node_modules" != item
        ):
            if os.path.isdir(item_path):
                # Check if README.md exists in this folder, create one if not
                read_me_file_list = mio.find_files_nc(current_dir, FILE_README)
                read_me_file = ""
                if not read_me_file_list:
                    global_logger.info(f"Cannot find {FILE_README}, will create...")
                    read_me_file = __create_empty_readme(current_dir)
                elif len(read_me_file_list) != 1:
                    global_logger.error(f"Multiple {FILE_README} files found")
                else:
                    global_logger.debug(f"Found one {FILE_README}")
                    read_me_file = read_me_file_list[0]
                # README.md should act as a branch node, with the name capitalized
                structure_name = item.capitalize()
                structure_path = __split_path_after_keyword(read_me_file, root_dir)
                line = f"{indent}* [{structure_name}]({structure_path})\n"
                summary_structure += line
                global_logger.debug(f"Added line: {line}")
                # Create REFERS.md if Other files exist
                found_others_file_list = mio.find_files_nc_without_extension(
                    item_path, FILE_EXTENSION_MD, FILE_EXTENSION_JSON
                )
                if found_others_file_list:
                    global_logger.info(
                        "Other file formats found, creating REFERS.md..."
                    )
                    refers_data = ""
                    for found_others_file in found_others_file_list:
                        structure_name = mio.get_basename(found_others_file)
                        strcuture_path = mio.get_filename_from_pathall(
                            found_others_file
                        )
                        refers_data += f"\n- [{structure_name}]({strcuture_path})"
                    refers_file_path_all = mio.join_file_path(item_path, FILE_REFERS)
                    mio.write_data_to_file(
                        refers_file_path_all,
                        refers_data,
                    )
                # Continue recursively
                summary_structure += __generate_readme_refers_summary(
                    root_dir, item_path, indent + INDENT
                )
            # If it's a .md note file, add it to the directory structure
            elif (
                item.endswith(FILE_EXTENSION_MD)
                and FILE_README != item
                and FILE_SUMMARY != item
            ):
                structure_name = item.replace(".md", "").replace("_", " ").capitalize()
                structure_path = __split_path_after_keyword(
                    mio.join_file_path(current_dir, item), root_dir
                )
                line = f"{indent}* [{structure_name}]({structure_path})\n"
                summary_structure += line
                global_logger.debug(f"Added line: {line}")
    return summary_structure


def workflow_generate_structured_md(dir):
    global global_logger
    from common.mlogger import global_logger

    global_logger.info("\nStart generating structured md...")

    __txt_to_md(dir)

    __clean_readme_refers(dir)

    summary_data = __generate_readme_refers_summary(dir, dir, INDENT)
    mio.write_data_to_file(
        mio.join_file_path(dir, FILE_SUMMARY),
        summary_data,
    )


if __name__ == "__main__":
    import common.mlogger

    common.mlogger.setup_console_file_logger()
    workflow_generate_structured_md(".")
    input("Press Any Button to Exit...")
