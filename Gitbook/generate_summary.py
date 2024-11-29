import os

from mio import (
    get_filepath_from_pathall,
)
from mlogger import global_logger

LIB_PATH = "D:\personal\CSBlogGitbook"


def split_path_after_keyword(path, keyword):
    parts = path.split(keyword, 1)
    if len(parts) > 1:
        splited_path = parts[1].lstrip(os.path.sep)
        return splited_path
    else:
        return None


def create_empty_readme(folder_path):
    """
    在指定文件夹中创建一个空的README.md文件

    参数:
    - folder_path: 指定的文件夹路径
    """
    readme_path = os.path.join(folder_path, "README.md")

    # 检查README.md文件是否已存在，如果不存在则创建
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# " + os.path.basename(folder_path).capitalize() + "\n\n")

    global_logger.debug(f"空的README.md已成功创建在 {folder_path}")


def find_readme_in_folder(folder_path):
    """
    在指定文件夹下查找README.md文件

    参数:
    - folder_path: 指定的文件夹路径

    返回:
    - readme_path: README.md文件的路径，如果找到的话；否则返回None
    """
    readme_path = os.path.join(folder_path, "README.md")

    if os.path.exists(readme_path):
        return readme_path
    else:
        return None


def create_summary(folder_path, summary_data):
    readme_path = os.path.join(folder_path, "SUMMARY.md")

    # 检查README.md文件是否已存在，如果不存在则创建
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(summary_data)

    global_logger.debug(f"SUMMARY.md已成功创建在 {folder_path}")


def generate_summary(folder_path, indent=""):
    """
    生成指定文件夹内的.md文件目录结构

    参数:
    - folder_path: 指定的文件夹路径
    - indent: 缩进字符串

    返回:
    - md_structure: 生成的.md文件目录结构
    """
    md_structure = ""

    # 遍历文件夹内的所有文件和子文件夹
    for item in sorted(os.listdir(folder_path)):
        item_path = os.path.join(folder_path, item)
        relative_path = split_path_after_keyword(item_path, LIB_PATH)
        global_logger.debug(relative_path)
        # 如果是文件夹，则递归生成子目录结构
        if (
            os.path.isdir(item_path)
            and "imgs" not in item_path
            and "files" not in item_path
        ):
            relative_file = os.path.join(relative_path, "README.md")
            readme_path = os.path.join(
                LIB_PATH, get_filepath_from_pathall(relative_file)
            )
            read_me_path = find_readme_in_folder(readme_path)
            if not read_me_path:
                global_logger.warning("找不到README.md")
                create_empty_readme(readme_path)
            # elif len(read_me_file_list) != 1:
            #     global_logger.error("找到多个README.md")
            else:
                global_logger.debug("找到了README.md")
            md_structure += f"{indent}* [{item.capitalize()}]({relative_file})\n"
            md_structure += generate_summary(item_path, indent + "   ")

        # 如果是.md文件，则添加到目录结构
        elif item.endswith(".md") and "README" not in item:
            # relative_file = os.path.join(relative_path, item)
            # if item == "README.md":
            #     md_structure += f"{indent}* [Introduction]({item})\n"
            # else:
            md_structure += f"{indent}* [{item.replace('.md', '').replace('_', ' ').capitalize()}]({relative_path})\n"

    return md_structure


if __name__ == "__main__":
    summary_data = generate_summary(LIB_PATH, "  ")
    global_logger.debug(summary_data)
    create_summary(LIB_PATH, summary_data)
    input("任意键退出")
