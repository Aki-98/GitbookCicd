from common.mlogger import global_logger

from common import mio
from common import mpic


def workflow_compress_imgs(file_path: str):
    global_logger.info("\nStart for compress imgs...")
    jpeg_file_list = mio.find_files_nc(file_path=file_path, file_name=".jpeg")
    jpg_file_list = mio.find_files(file_path=file_path, file_name=".jpg")
    jpg_file_list += jpeg_file_list
    png_file_list = mio.find_files(file_path=file_path, file_name=".png")
    for jpg_file in jpg_file_list:
        file_size_mb_before = mio.get_file_size_mb(jpg_file)
        global_logger.debug(f"jpg file: {jpg_file}")
        global_logger.debug(f"file size before {file_size_mb_before:.2f} MB")
        if file_size_mb_before > 1:
            mpic.compress_jpg(jpg_file, jpg_file, quality=30)
            file_size_mb_after = mio.get_file_size_mb(jpg_file)
            global_logger.debug(f"file size after {file_size_mb_after:.2f} MB")
        else:
            global_logger.debug(f"file with a small size skip for compressing")

    for png_file in png_file_list:
        file_size_mb_before = mio.get_file_size_mb(png_file)
        global_logger.debug(f"png file: {png_file}")
        global_logger.debug(f"file size before {file_size_mb_before:.2f} MB")
        if file_size_mb_before > 0.5:
            mpic.compress_png(png_file, png_file)
            file_size_mb_after = mio.get_file_size_mb(png_file)
            global_logger.debug(f"file size after {file_size_mb_after:.2f} MB")
        else:
            global_logger.debug(f"file with a small size skip for compressing")


if __name__ == "__main__":
    import common.mlogger

    common.mlogger.setup_console_file_logger()

    workflow_compress_imgs(".")
    input("Press Any Button to Exit...")
