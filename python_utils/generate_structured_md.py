from mlogger import global_logger
import os
import mio

FILE_README = "README.md"
FILE_SUMMARY = "SUMMARY.md"
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
        global_logger.debug(f"item: {item}")
        # 如果是文件夹, 并且不为存放imgs和files的文件夹, 则递归生成子目录结构
        if (
            "imgs" not in item_path
            and "files" not in item_path
            and ".git" not in item_path
            and "node_modules" not in item_path
        ):
            if os.path.isdir(item_path):
                # 找下这个文件夹里有无README.md, 没有则需要创建
                read_me_file_list = mio.find_files_nc(current_dir, FILE_README)
                read_me_file = ""
                if not read_me_file_list:
                    global_logger.warning(f"找不到{FILE_README}")
                    __create_empty_readme(current_dir)
                    read_me_file = mio.join_file_path(current_dir, FILE_README)
                elif len(read_me_file_list) != 1:
                    global_logger.error(f"找到多个{FILE_README}")
                else:
                    global_logger.debug(f"找到了一个{FILE_README}")
                    read_me_file = read_me_file_list[0]
                # README.md 应作为枝干节点, 名称的首字母转为大写
                structure_name = item.capitalize()
                structure_path = __split_path_after_keyword(read_me_file, root_dir)
                line = f"{indent}* [{structure_name}]({structure_path})\n"
                global_logger.debug(f"add line: {line}")
                summary_structure += line
                # 继续递归查找
                summary_structure += __generate_summary_and_readme(
                    root_dir, item_path, indent + INDENT
                )
            # 如果是笔记.md文件，则添加到目录结构
            elif item.endswith(FILE_EXTENSION_MD) and "README" not in item:
                structure_name = item.replace(".md", "").replace("_", " ").capitalize()
                structure_path = __split_path_after_keyword(
                    mio.join_file_path(current_dir, item), root_dir
                )
                line = f"{indent}* [{structure_name}]({structure_path})\n"
                global_logger.debug(f"add line: {line}")
                summary_structure += line
    return summary_structure


def __append_other_files_to_md(root_dir):
    readme_pathall_list = mio.find_files(root_dir, FILE_README)
    for readme_pathall in readme_pathall_list:
        readme_folder = mio.get_filepath_from_pathall(readme_pathall)
        found_others_file_list = mio.find_files_nc_without_extension(
            readme_folder, [FILE_EXTENSION_MD, FILE_EXTENSION_JSON]
        )
        if not found_others_file_list:
            global_logger.debug("没有找到其他格式的文件，不需要重写README.md")
        else:
            global_logger.debug("重写README.md...")
            readme_data = ""
            for found_others_file in found_others_file_list:
                structure_name = mio.get_basename(found_others_file)
                strcuture_path = structure_name
                readme_data = f"\n[{structure_name}]({strcuture_path})"
            mio.write_data_to_file(
                readme_pathall, r"> 文件索引" + readme_data + "\n" + r"索引结束 <"
            )


def workflow_generate_structured_md(dir):
    __txt_to_md(dir)
    summary_data = __generate_summary_and_readme(dir, dir, INDENT)
    global_logger.info(summary_data)
    mio.write_data_to_file(mio.join_file_path(dir, FILE_SUMMARY), summary_data)
    __append_other_files_to_md(dir)


if __name__ == "__main__":
    workflow_generate_structured_md(".")
    input("任意键退出")
