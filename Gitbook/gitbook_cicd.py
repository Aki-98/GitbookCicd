import mio
import mpic
from mlogger import global_logger


def workflow_compress_ismgs():
    """
    压缩图片: 只支持jpg、jpeg和png
    """
    jpeg_file_list = mio.find_files(file_name=".jpeg")
    jpg_file_list = mio.find_files(file_name=".jpg")
    jpg_file_list += jpeg_file_list
    png_file_list = mio.find_files(file_name=".png")
    for jpg_file in jpg_file_list:
        file_size_mb_before = mio.get_file_size_mb(jpg_file)
        global_logger.debug(f"jpg file: {jpg_file}")
        global_logger.debug(f"file size before {file_size_mb_before:.2f} MB")
        if file_size_mb_before > 1:
            mpic.compress_jpg(jpg_file, jpg_file, quality=30)
        else:
            mpic.compress_jpg(jpg_file, jpg_file, quality=95)
        file_size_mb_after = mio.get_file_size_mb(jpg_file)
        global_logger.debug(f"file size after {file_size_mb_after:.2f} MB")
    for png_file in png_file_list:
        file_size_mb_before = mio.get_file_size_mb(png_file)
        global_logger.debug(f"png file: {png_file}")
        global_logger.debug(f"file size before {file_size_mb_before:.2f} MB")
        mpic.compress_png(png_file, png_file)
        file_size_mb_after = mio.get_file_size_mb(png_file)
        global_logger.debug(f"file size after {file_size_mb_after:.2f} MB")


def workflow_txt_to_md():
    """
    将txt文件转为md文件
    """
    txt_file_list = mio.find_files(file_name=".txt")
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
