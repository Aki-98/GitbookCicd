import mio
from mlogger import global_logger


def workflow_txt_to_md(file_path: str):
    """
    将txt文件转为md文件
    """
    global_logger.debug(
        "-----------------------workflow_txt_to_md-----------------------"
    )
    txt_file_list = mio.find_files(file_path=file_path, file_name=".txt")
    for txt_file in txt_file_list:
        global_logger.debug(f"found txt file: {txt_file}")
        txt_file_path = mio.get_filepath_from_pathall(txt_file)
        txt_file_name = mio.get_filename_from_pathall(txt_file)
        md_file_name = txt_file_name.replace(".txt", ".md")
        mio.copy_files(
            from_folder_path=txt_file_path,
            from_file_name_or_format=txt_file_name,
            to_folder_path=txt_file_path,
            to_file_name=md_file_name,
        )
        global_logger.debug(f"to md file: {md_file_name}")
        mio.delete_files(file_path=txt_file_path, file_name_or_format=txt_file_name)
        global_logger.debug(f"delete txt file succeed")


if __name__ == "__main__":
    workflow_txt_to_md(".")
