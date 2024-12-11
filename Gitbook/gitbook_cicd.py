import mio
import mlogger
import mterminal
import mgit
from mlogger import global_logger

import compress_img
import reformat_imgs_in_md
import generate_structured_md

LIB_GITBOOK = "Gitbook"


def workflow_cicd_commit(lib_name: str, lib_dir_gitbook: str, rename: bool):
    lib_path = mio.join_file_path(root_repo_path, lib_name)
    global_logger.debug("[lib_path]: " + lib_path)
    git_status_file_list = mgit.get_git_status_files(lib_path)
    # {}会创建一个set
    changed_folder_list = {
        mio.get_filepath_from_pathall(file_path) for file_path in git_status_file_list
    }
    for changed_folder in changed_folder_list:
        # 压缩图片
        compress_img.workflow_compress_imgs(changed_folder)
        # 修改md中的图片引用格式
        reformat_imgs_in_md.workflow_reformat_imgs_in_md(changed_folder, rename)
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
    workflow_cicd_commit("CSGitbook", "cs", True)
    workflow_cicd_commit("CSBlogGitbook", "csblog", True)
    workflow_cicd_commit("KnowGitbook", "know", False)
    input("任意键退出")
