import mio
import mlogger
import mterminal
from mlogger import global_logger

import compress_img
import reformat_imgs_in_md
import generate_structured_md

LIB_GITBOOK = "Gitbook"


def workflow_cicd_all(lib_name: str, lib_dir_gitbook: str, rename: bool):
    lib_path = mio.join_file_path(root_repo_path, lib_name)
    global_logger.debug("[lib_path]: " + lib_path)
    # 压缩图片
    compress_img.workflow_compress_imgs(lib_path)
    # 修改md中的图片引用格式
    reformat_imgs_in_md.workflow_reformat_imgs_in_md(lib_path, rename)
    # 生成SUMMARY.md和README.md
    generate_structured_md.workflow_generate_structured_md(lib_path)
    # 清除空文件夹
    mio.remove_empty_folders(lib_path)
    # 删除_book & Gitbook\{book}
    lib_book_path = mio.join_file_path(root_repo_path, lib_name, "_book")
    global_logger.debug("[lib_book_path]: " + lib_book_path)
    mio.delete_files(lib_book_path)
    lib_dir_book_path = mio.join_file_path(root_repo_path, LIB_GITBOOK, lib_dir_gitbook)
    global_logger.debug("[lib_dir_book_path]: " + lib_dir_book_path)
    mio.delete_files(lib_dir_book_path)
    # gitbook build
    mterminal.run_command(lib_path, ["gitbook", "build"])
    # Copy gitbook
    mio.copy_folder(lib_book_path, lib_dir_book_path)


if __name__ == "__main__":
    execution_path = mlogger.get_cwd()
    root_repo_path = mio.rollback_path(execution_path, 1)
    workflow_cicd_all("CSGitbook", "cs", True)
    workflow_cicd_all("CSBlogGitbook", "csblog", True)
    workflow_cicd_all("KnowGitbook", "know", False)
    input("任意键退出")
