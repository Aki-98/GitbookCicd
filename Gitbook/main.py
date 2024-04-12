import os
import re

from mio import (
    find_files,
    copy_files,
    delete_files,
    get_filepath_from_pathall,
    get_filename_from_pathall,
    read_data_from_file,
    write_data_to_file,
)
from minput import exit_or_continue
from mlogger import global_logger

LIB_PATH = "D:\personal\CSGitbook"
IMG_FORMAT = r"!\[.*?\]\((.*?)\)"


def txt_to_md(lib_path):
    txt_file_list = find_files(file_path=lib_path, file_name=".txt")
    for txt_file in txt_file_list:
        global_logger.debug(f"found txt file: {txt_file}")
        txt_file_path = get_filepath_from_pathall(txt_file)
        txt_file_name = get_filename_from_pathall(txt_file)
        md_file_name = txt_file_name.replace(".txt", ".md")
        copy_files(
            from_folder_path=txt_file_path,
            from_file_name_or_format=txt_file_name,
            to_folder_path=txt_file_path,
            to_file_name=md_file_name,
        )
        global_logger.debug(f"to md file: {md_file_name}")
        delete_files(file_path=txt_file_path, file_name_or_format=txt_file_name)
        global_logger.debug(f"delete txt file succeed")


def find_image_references_in_md(md_data):
    matches = re.findall(IMG_FORMAT, md_data)
    return matches


def split_path_after_keyword(path, keyword):
    parts = path.split(keyword, 1)
    if len(parts) > 1:
        splited_path = parts[1].lstrip(os.path.sep)
        return splited_path
    else:
        return None


def get_md_file_list(lib_path):
    md_file_list = find_files(file_path=lib_path, file_name=".md")
    return md_file_list


def img_to_folder(md_file_list):
    for md_file_path_all in md_file_list:
        global_logger.debug(f"_________________________我是分割线_____________________")
        global_logger.debug(f"found md file: {md_file_path_all}")
        md_name = get_filename_from_pathall(md_file_path_all).replace(".md", "")
        md_path = get_filepath_from_pathall(md_file_path_all)
        md_data = read_data_from_file(file_all_path=md_file_path_all)
        img_ref_list = find_image_references_in_md(md_data)
        is_refs_changed = False
        for img_ref in img_ref_list:
            global_logger.debug(f"found img ref: {img_ref}")
            if md_name + "_imgs" == get_filepath_from_pathall(img_ref):
                global_logger.debug("图片引用已经用了正确的格式")
            else:
                is_refs_changed = True
                global_logger.warning("图片引用没有使用正确的格式")
                global_logger.debug("开始查找图片")
                img_file_name = get_filename_from_pathall(img_ref)
                if "http" in img_ref:
                    global_logger.error("网络图片，去下载另存")
                if "CSLibrary" in img_ref:
                    relative_path = split_path_after_keyword(img_ref, "CSLibrary")
                    global_logger.debug(f"绝对路径: {relative_path}")
                elif "CSGitbook" in img_ref:
                    relative_path = split_path_after_keyword(img_ref, "CSGitbook")
                    global_logger.debug(f"绝对路径: {relative_path}")
                else:
                    relative_path = os.path.join(md_path, img_file_name)
                    global_logger.debug(f"相对路径: {relative_path}")

                correct_absolute_path = os.path.join(LIB_PATH, relative_path)
                img_path = get_filepath_from_pathall(correct_absolute_path)
                img_name = get_filename_from_pathall(correct_absolute_path)
                found_img_list = find_files(file_path=img_path, file_name=img_name)
                global_logger.debug(f"found img list {found_img_list}")
                if len(found_img_list) == 0:
                    global_logger.warning("绝对路径找不到图片, 转为按文件名查找")
                    found_img_list = find_files(
                        file_path=LIB_PATH, file_name=img_file_name
                    )
                    if len(found_img_list) == 0:
                        global_logger.error("按文件名也找不到文件")
                    elif len(found_img_list) != 1:
                        global_logger.error("按文件名找到多张图片")
                elif len(found_img_list) != 1:
                    global_logger.error("找到多张图片")

                found_img_path_all = found_img_list[0]
                found_img_path = get_filepath_from_pathall(found_img_path_all)
                # 复制图片
                _, img_format = os.path.splitext(img_file_name)
                md_img_folder = os.path.join(md_path, md_name + "_imgs")
                global_logger.debug(f"img format: {img_format}")
                if found_img_path != md_img_folder:
                    global_logger.debug(f"img文件路径不一致，开始复制")
                    if img_format:
                        # 复制图片
                        copy_files(
                            from_folder_path=found_img_path,
                            from_file_name_or_format=img_file_name,
                            to_folder_path=md_img_folder,
                            to_file_name=img_file_name,
                        )
                        # 删除图片
                        delete_files(
                            file_path=found_img_path, file_name_or_format=img_file_name
                        )
                    else:
                        # 复制图片
                        copy_files(
                            from_folder_path=found_img_path,
                            from_file_name_or_format=img_file_name,
                            to_folder_path=md_img_folder,
                            to_file_name=img_file_name + ".png",
                        )
                        # 删除图片
                        delete_files(
                            file_path=found_img_path, file_name_or_format=img_file_name
                        )
                        img_file_name = img_file_name + ".png"
                        exit_or_continue()
                else:
                    global_logger.debug(f"img文件路径一致")
                    exit_or_continue()
                # 修改md中的引用
                md_data = md_data.replace(
                    img_ref, os.path.join(md_name + "_imgs", img_file_name)
                )
        if is_refs_changed:
            global_logger.debug(f"修改md文件中的引用{md_file_path_all}")
            write_data_to_file(file_all_path=md_file_path_all, data=md_data)
            exit_or_continue()


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
        relative_path = split_path_after_keyword(item_path, "CSGitbook")
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


FORMAT_OTHERS = [".reg", ".pdf", ".docx"]


def find_files_in_folder(folder_path, file_extension):
    """
    在指定文件夹下查找指定格式的文件

    参数:
    - folder_path: 指定的文件夹路径
    - file_extension: 指定的文件格式，例如 '.md'

    返回:
    - files: 符合条件的文件列表
    """
    files = [
        f
        for f in os.listdir(folder_path)
        if f.endswith(file_extension) and os.path.isfile(os.path.join(folder_path, f))
    ]
    return files


def generate_readme():
    readme_pathall_list = find_files(LIB_PATH, "README.md")
    for readme_pathall in readme_pathall_list:
        global_logger.debug(f"_________________________我是分割线_____________________")
        global_logger.debug(f"readme path all: {readme_pathall}")
        readme_folder = get_filepath_from_pathall(readme_pathall)
        found_others_file_list = []
        for format in FORMAT_OTHERS:
            file_list = find_files_in_folder(readme_folder, format)
            found_others_file_list += file_list
        if len(found_others_file_list) == 0:
            global_logger.debug("没有找到其他格式的文件，不需要重写README.md")
        else:
            global_logger.debug("重写README.md...")
            readme_data = read_data_from_file(readme_pathall)
            for found_others_file in found_others_file_list:
                global_logger.debug(found_others_file)
                readme_data += f"\n[{found_others_file}]({found_others_file})"
            write_data_to_file(readme_pathall, readme_data)
            exit_or_continue()
    return True


if __name__ == "__main__":
    # txt_to_md(LIB_PATH)
    # md_file_list = get_md_file_list(LIB_PATH)
    # img_to_folder(md_file_list)
    # summary_data = generate_summary(LIB_PATH, "  ")
    # global_logger.debug(summary_data)
    # create_summary(LIB_PATH, summary_data)
    generate_readme()
    input("任意键退出")
