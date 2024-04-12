from os import path, makedirs, walk, remove
from shutil import rmtree, copy, copytree
from json import load, dumps
from zipfile import ZipFile, ZIP_DEFLATED

from mcommon import ENCODE, run_command
from minput import exit_or_continue
from mlogger import global_logger

# ----------------------------- 文件读写 -----------------------------


def write_data_to_file(file_all_path, data):
    try:
        file_parent_path = path.dirname(file_all_path)
        # 检查目录是否存在
        # TODO: 解决只传入文件名，写入到当前路径的问题，待验证
        if file_parent_path:
            if not path.exists(file_parent_path):
                # 如果目录不存在，使用 os.makedirs 创建路径
                makedirs(file_parent_path)
                global_logger.info(f"path has been created: {file_parent_path}")
            # 打开文件并以写入模式写入数据,会清空之前的数据
        with open(file_all_path, "w", encoding=ENCODE) as file:
            file.write(str(data))
        # global_logger.debug(f"[write_data_to_file] 数据已成功写入文件：{data}")
    except Exception as e:
        global_logger.error(f"error: {e}")
        exit_or_continue()


def append_data_to_file(file_all_path, data):
    try:
        file_parent_path = path.dirname(file_all_path)
        # 检查目录是否存在
        if not path.exists(file_parent_path):
            # 如果目录不存在，使用 os.makedirs 创建路径
            makedirs(file_parent_path)
            global_logger.info(f"path has been created: {file_parent_path}")
        # 打开文件并以追加模式写入数据,不会清空之前的数据
        with open(file_all_path, "a", encoding=ENCODE) as file:
            file.write(str(data))
        # global_logger.debug(f"[append_data_to_file] 数据已成功写入文件：{data}")
    except Exception as e:
        global_logger.error(f"error: {e}")
        exit_or_continue()


def read_data_from_file(file_all_path):
    try:
        # 打开文件并以读取模式读取数据
        with open(file_all_path, "r", encoding=ENCODE) as file:
            data = file.read()
        # global_logger.debug(f"[read_data_from_file] 成功从文件读取数据：{data}")
        return data
    except Exception as e:
        global_logger.error(f"error: {e}")
        exit_or_continue()


# ----------------------------- JSON读写 -----------------------------


def get_json_from_file(file_all_path):
    """
    从Json文件读取Json
    """
    try:
        with open(file_all_path, "r", encoding=ENCODE) as file:
            json_data = load(file)
        return json_data
    except Exception as e:
        global_logger.warning(f"error: {e}")
        return None


def write_json_to_file(file_all_path, json_data):
    """
    将Json文件写入目标文件
    """
    try:
        json_data = dumps(json_data, indent=4, ensure_ascii=False)
        write_data_to_file(file_all_path, json_data)
    except Exception as e:
        global_logger.error(f"error: {e}")


# ----------------------------- 文件查询 -----------------------------


def find_files(file_path="", file_name=".apk", filter=""):
    """
    通过文件后缀获取所有文件，需要遍历文件树，传入的文件后缀需要以.开始，默认搜索apk文件
    如果寻找某个文件格式的文件，那么返回列表，如果寻找某个文件，那么返回单个文件路径
    """
    try:
        # 根据关键字搜索文件
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
        # 搜索某一文件格式的文件
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
        # 搜索某个文件
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
        global_logger.error(f"error: {e}")
    # 如果没有找到，则返回None
    return None


# ----------------------------- 删除文件 -----------------------------


def delete_files(file_path="", file_name_or_format=""):
    """
    删除文件，默认有三种方式：删除所有文件、删除文件树下所有属于某个文件格式的文件、删除某个文件
    """
    try:
        # 不指定要删除的文件，则删除所有文件
        if "" == file_name_or_format:
            # 递归删除文件夹及其内容
            global_logger.debug(f"delete all file in folder {file_path}")
            rmtree(file_path)
        # 如果传入的是文件格式，则递归删除特定文件格式的文件
        elif file_name_or_format.startswith("."):
            global_logger.debug(
                f"delete file of format {file_name_or_format} in folder {file_path}"
            )
            found_files = find_files(file_path, file_name_or_format)
            for file in found_files:
                remove(file)
        # 删除某个文件
        else:
            global_logger.debug(
                f"delete file of name {file_name_or_format} in folder {file_path}"
            )
            remove(join_file_path(file_path, file_name_or_format))
        global_logger.info(f"succeed!")
    except Exception as e:
        global_logger.error(f"error: {e}")


# ----------------------------- 复制文件 -----------------------------


def copy_files(
    from_folder_path="/",
    from_file_name_or_format="",
    to_folder_path="/",
    to_file_name="",
):
    """
    复制文件，默认有三种方式：复制所有文件、复制文件树下所有属于某个文件格式的文件、复制某个文件
    """
    try:
        # 不指定要复制的文件，则复制所有文件
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
        # 如果传入的是文件格式，则复制特定文件格式的文件
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
        # 复制某个文件
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


# ----------------------------- 压缩文件 -----------------------------


def zip_file(file_path, zip_path):
    zip_file = ZipFile(zip_path, "w")
    zip_file.write(
        file_path,
        compress_type=ZIP_DEFLATED,
        arcname=get_filename_from_pathall(file_path),
    )
    zip_file.close()


PATH_WINRAR = "F:\winrar\WinRAR.exe"


def rar_file(work_directory, file_name, rar_name):
    """
    work_directory: 启动winrar.exe的工作路径
    file_name: 输入文件的名字
    rar_name: 输出的rar的名字
    """
    run_command(work_directory, [PATH_WINRAR, "a", rar_name, file_name])


# ----------------------------- 工具方法 -----------------------------


def get_filename_from_pathall(file_path_all):
    return path.basename(file_path_all)


def get_filepath_from_pathall(file_path_all):
    return path.dirname(file_path_all)


def join_file_path(*args):
    if "" == args[0]:
        return path.join(args[1:])
    return path.join(*args)


def is_file_exist(path_all_file):
    return path.exists(path_all_file)
