import argparse

from common import mio
from common import mlogger
from common import mterminal

import compress_img
import reformat_imgs_in_md
import generate_structured_md

DESCRIPTION = """
This script automates tasks to prepare your GitBook repository for building.

What it does:
- Generate README.md and SUMMARY.md:
  Generates README.md files for sub directories and a SUMMARY.md file in the root directory.
  (if they don't already exist).
- Create REFERS.md:
  Creates a REFERS.md file for any documents (not Markdown files and images) that exist.
- Download web pictures:(Default-false)
  Downloads pictures referenced in your Markdown files and saves them to the GitBook repository.
- Reorganize local pictures:(Default-true)
  Moves local pictures referenced in your Markdown files to the directory at the same level as the md file directory.
  (Please ensure images are already placed within the repository).
- Optimize pictures:(Default-false)
  Optimizes pictures to reduce file size without significant quality loss.

Notice:
- Please run this script from the root directory of your GitBook repository.
"""


def __prebook_all(
    download_imgs: bool,
    reorganize_imgs: bool,
    optimize_imgs: bool,
    log_to_file: bool,
):
    print("Executing for all files...")
    print(f"Options:")
    print(f"  Download Images: {download_imgs}")
    print(f"  Reorganize Images: {reorganize_imgs}")
    print(f"  Optimize Images: {optimize_imgs}")
    print(f"  Log to File: {log_to_file}")
    # lib_path = mio.join_file_path(root_repo_path, lib_name)
    # global_logger.debug("[lib_path]: " + lib_path)
    # # 压缩图片, 可选
    # compress_img.workflow_compress_imgs(lib_path)
    # # 修改md中的图片引用格式, 移动图片位置
    # reformat_imgs_in_md.workflow_reformat_imgs_in_md(lib_path, rename)
    # # 生成SUMMARY.md和README.md
    # generate_structured_md.workflow_generate_structured_md(lib_path)
    # # 清除空文件夹
    # mio.remove_empty_folders(lib_path)
    # # 清除无效的README.md
    # # 删除_book & Gitbook\{book}
    # lib_book_path = mio.join_file_path(root_repo_path, lib_name, "_book")
    # global_logger.debug("[lib_book_path]: " + lib_book_path)
    # mio.delete_files(lib_book_path)
    # lib_dir_book_path = mio.join_file_path(root_repo_path, LIB_GITBOOK, lib_dir_gitbook)
    # global_logger.debug("[lib_dir_book_path]: " + lib_dir_book_path)
    # mio.delete_files(lib_dir_book_path)
    # # gitbook build
    # mterminal.run_command(lib_path, ["gitbook", "build"])
    # # Copy gitbook
    # mio.copy_folder(lib_book_path, lib_dir_book_path)


def __prebook_diff(
    download_imgs: bool,
    reorganize_imgs: bool,
    optimize_imgs: bool,
    log_to_file: bool,
):
    print("Executing for files different from last commit...")
    print(f"Options:")
    print(f"  Download Images: {download_imgs}")
    print(f"  Reorganize Images: {reorganize_imgs}")
    print(f"  Optimize Images: {optimize_imgs}")
    print(f"  Log to File: {log_to_file}")
    # lib_path = mio.join_file_path(root_repo_path, lib_name)
    # global_logger.debug("[lib_path]: " + lib_path)
    # git_status_file_list = mgit.get_git_status_files(lib_path)
    # # {}会创建一个set
    # changed_folder_list = {
    #     mio.get_filepath_from_pathall(file_path) for file_path in git_status_file_list
    # }
    # for changed_folder in changed_folder_list:
    #     # 压缩图片
    #     compress_img.workflow_compress_imgs(changed_folder)
    #     # 修改md中的图片引用格式
    #     reformat_imgs_in_md.workflow_reformat_imgs_in_md(changed_folder, rename)
    # # 生成SUMMARY.md和README.md
    # generate_structured_md.workflow_generate_structured_md(lib_path)
    # # 清除空文件夹
    # mio.remove_empty_folders(lib_path)
    # # 删除_book & Gitbook\{book}
    # lib_book_path = mio.join_file_path(root_repo_path, lib_name, "_book")
    # global_logger.debug("[lib_book_path]: " + lib_book_path)
    # mio.delete_files(lib_book_path)
    # lib_dir_book_path = mio.join_file_path(root_repo_path, LIB_GITBOOK, lib_dir_gitbook)
    # global_logger.debug("[lib_dir_book_path]: " + lib_dir_book_path)
    # mio.delete_files(lib_dir_book_path)
    # # gitbook build
    # mterminal.run_command(lib_path, ["gitbook", "build"])
    # # Copy gitbook
    # mio.copy_folder(lib_book_path, lib_dir_book_path)


def main():
    # 主解析器
    parser = argparse.ArgumentParser(
        prog="prebook", description=("Pre-build setup for GitBook")
    )
    parser.add_argument(
        "--details", action="store_true", help="Show Detailed Introduction"
    )

    # 创建子命令解析器
    subparsers = parser.add_subparsers(
        dest="command", help="all available sub commands"
    )

    # 子命令: all
    parser_all = subparsers.add_parser("all", help="Execute for all files")

    # 子命令: diff
    parser_diff = subparsers.add_parser(
        "diff", help="Execute for files differs from last commit"
    )

    parser.add_argument(
        "-d", "--download-imgs", action="store_true", help="Download web pictures"
    )
    parser.add_argument(
        "-r",
        "--reorganize-imgs",
        action="store_false",
        help="Reorganize local pictures",
    )
    parser.add_argument(
        "-o", "--optimize-imgs", action="store_true", help="Compress jpgs and pngs"
    )
    parser.add_argument(
        "-l", "--log-to-file", action="store_true", help="Output log to a file"
    )

    # 解析并处理命令
    args = parser.parse_args()
    if args.details:
        print(DESCRIPTION)
    elif args.command == "all":
        __prebook_all(
            args.download_imgs,
            args.reorganize_imgs,
            args.optimize_imgs,
            args.log_to_file,
        )
    elif args.command == "diff":
        __prebook_diff(
            args.download_imgs,
            args.reorganize_imgs,
            args.optimize_imgs,
            args.log_to_file,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
