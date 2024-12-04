from mlogger import global_logger
import os
import mio

FILE_README = "README.md"
FILE_SUMMARY = "SUMMARY.md"
FILE_EXTENSION_MD = ".md"
FILE_EXTENSION_TXT = ".txt"
INDENT = "  "


def __split_path_after_keyword(path, keyword):
    parts = path.split(keyword, 1)
    if len(parts) > 1:
        splited_path = parts[1].lstrip(os.path.sep)
        return splited_path
    else:
        return None


def __find_files_without_extension(folder_path, without_file_extension):
    files = [
        f
        for f in os.listdir(folder_path)
        if not f.endswith(without_file_extension)
        and os.path.isfile(os.path.join(folder_path, f))
    ]
    return files


def __create_empty_readme(folder_path):
    readme_path = os.path.join(folder_path, "README.md")

    # 检查README.md文件是否已存在，如果不存在则创建
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# " + os.path.basename(folder_path).capitalize() + "\n\n")

    global_logger.debug(f"空的README.md已成功创建在 {folder_path}")


def __txt_to_md(file_path: str):
    txt_file_list = mio.find_files(file_path=file_path, file_name=FILE_EXTENSION_TXT)
    for txt_file in txt_file_list:
        global_logger.debug(f"found txt file: {txt_file}")
        txt_file_path = mio.get_filepath_from_pathall(txt_file)
        txt_file_name = mio.get_filename_from_pathall(txt_file)
        md_file_name = txt_file_name.replace(FILE_EXTENSION_TXT, FILE_EXTENSION_MD)
        mio.copy_files(
            from_folder_path=txt_file_path,
            from_file_name_or_format=txt_file_name,
            to_folder_path=txt_file_path,
            to_file_name=md_file_name,
        )
        global_logger.debug(f"to md file: {md_file_name}")
        mio.delete_files(file_path=txt_file_path, file_name_or_format=txt_file_name)
        global_logger.debug(f"delete txt file succeed")


def __generate_summary_and_readme(root_dir, current_dir, indent):
    """
    递归生成指定文件夹内的.md文件目录结构

    参数:
    - folder_path: 指定的文件夹路径
    - indent: 缩进字符串

    返回:
    - md_structure: 生成的.md文件目录结构
    """
    summary_structure = ""

    # 遍历文件夹内的所有文件和子文件夹
    for item in os.listdir(current_dir):
        item_path = mio.join_file_path(current_dir, item)
        # 如果是文件夹, 并且不为存放imgs和files的文件夹, 则递归生成子目录结构
        if (
            os.path.isdir(item_path)
            and "imgs" not in item_path
            and "files" not in item_path
        ):
            # 找下这个文件夹里有无README.md, 没有则需要创建
            read_me_file_list = mio.find_files_nc(current_dir, FILE_README)
            if not read_me_file_list:
                global_logger.warning("找不到README.md")
                __create_empty_readme(current_dir)
            elif len(read_me_file_list) != 1:
                global_logger.error("找到多个README.md")
            else:
                global_logger.debug("找到了一个README.md")
            # README.md 应作为枝干节点, 名称的首字母转为大写
            structure_name = item.capitalize()
            structure_path = __split_path_after_keyword(read_me_file_list[0], root_dir)
            summary_structure += f"{indent}* [{structure_name}]({structure_path})\n"
            # 继续递归查找
            summary_structure += __generate_summary_and_readme(
                item_path, indent + INDENT
            )
        # 如果是笔记.md文件，则添加到目录结构
        elif item.endswith(FILE_EXTENSION_MD) and "README" not in item:
            structure_name = item.replace(".md", "").replace("_", " ").capitalize()
            strcuture_path = __split_path_after_keyword(item, root_dir)
            summary_structure += f"{indent}* [{structure_name}]({strcuture_path})\n"
        else:
            global_logger.debug("跳过存放imgs和files的文件夹")
    return summary_structure


def __write_summary_md(folder_path, summary_data):
    readme_path = os.path.join(folder_path, FILE_SUMMARY)

    # 检查README.md文件是否已存在，如果不存在则创建
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(summary_data)

    global_logger.debug(f"{FILE_SUMMARY}已成功创建在 {folder_path}")


def __append_other_files_to_md(root_dir):
    readme_pathall_list = mio.find_files(root_dir, FILE_README)
    for readme_pathall in readme_pathall_list:
        readme_folder = mio.get_filepath_from_pathall(readme_pathall)
        found_others_file_list = __find_files_without_extension(
            readme_folder, FILE_EXTENSION_MD
        )
        if not found_others_file_list:
            global_logger.debug("没有找到其他格式的文件，不需要重写README.md")
        else:
            global_logger.debug("重写README.md...")
            readme_data = mio.read_data_from_file(readme_pathall)
            for found_others_file in found_others_file_list:
                structure_name = mio.get_basename(found_others_file)
                strcuture_path = structure_name
                readme_data += f"\n[{structure_name}]({strcuture_path})"
            mio.write_data_to_file(readme_pathall, readme_data)


def workflow_generate_structured_md(dir):
    __txt_to_md(dir)
    summary_data = __generate_summary_and_readme(dir, INDENT)
    __write_summary_md(dir, summary_data)
    __append_other_files_to_md(dir)


if __name__ == "__main__":
    workflow_generate_structured_md(".")
    input("任意键退出")
