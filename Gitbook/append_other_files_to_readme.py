import os

from mio import (
    find_files,
    get_filepath_from_pathall,
    read_data_from_file,
    write_data_to_file,
)
from minput import exit_or_continue
from mlogger import global_logger

LIB_PATH = "D:\personal\KnowGitbook"

FORMAT_OTHERS = [".reg", ".pdf", ".docx",".aep"]


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


def generate_readme(lib_path):
    readme_pathall_list = find_files(lib_path, "README.md")
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
    generate_readme(LIB_PATH)
    input("任意键退出")
