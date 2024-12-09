import mio
import mlogger

from mlogger import global_logger

import compress_img
import reformat_imgs_in_md
import generate_structured_md

LIB_DIR = {"CSGitbook": "cs", "CSBlogGitbook": "csblog", "KnowGitbook": "know"}
LIB_GITBOOK = "Gitbook"

if __name__ == "__main__":
    execution_path = mlogger.get_cwd()
    root_repo_path = mio.rollback_path(execution_path, 1)
    for lib_name, lib_dir_gitbook in LIB_DIR.items():
        lib_path = mio.join_file_path(root_repo_path, lib_name)
        global_logger.debug("[lib_path]: " + lib_path)
        lib_dir_gitbook_path = mio.join_file_path(
            root_repo_path, LIB_GITBOOK, lib_dir_gitbook
        )
        global_logger.debug("[lib_dir_gitbook_path]: " + lib_dir_gitbook_path)
        # 压缩图片
        compress_img.workflow_compress_imgs(lib_path)
        # 修改md中的图片引用格式
        reformat_imgs_in_md.workflow_reformat_imgs_in_md(lib_path)
        # 生成SUMMARY.md和README.md
        generate_structured_md.workflow_generate_structured_md(lib_path)
        # 清除空文件夹
        mio.remove_empty_folders(lib_path)
        # 删除_book
        # gitbook build
        mio.delete_files(lib_dir_gitbook_path)
    input("任意键退出")
