import argparse
import os

from common import mio
from common import mgit
from common import mlogger

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
    reorganize_imgs: bool,
    download_imgs: bool,
    rename_imgs: bool,
    optimize_imgs: bool,
    log_to_file: bool,
):
    if log_to_file:
        mlogger.setup_console_file_logger()
    else:
        mlogger.setup_console_logger()
    from common.mlogger import global_logger

    global_logger.info("Executing for all files...")
    global_logger.info(f"Options:")
    global_logger.info(f"  Reorganize Images: {reorganize_imgs}")
    global_logger.info(f"  Download Images: {download_imgs}")
    global_logger.info(f"  Rename Images: {rename_imgs}")
    global_logger.info(f"  Optimize Images: {optimize_imgs}")
    global_logger.info(f"  Log to File: {log_to_file}")
    # gitbook_path = mio.join_file_path("E:\.personal\CSGitbook")
    gitbook_path = "E:\.personal\\temp"
    global_logger.debug(f"Gitbook Path:" + gitbook_path)
    # 修改md中的图片引用格式, 移动图片位置, 下载md图片
    reformat_imgs_in_md.workflow_reformat_imgs_in_md(
        gitbook_path,
        reorganize_imgs,
        download_imgs,
        rename_imgs,
    )
    # 压缩图片, 可选
    if optimize_imgs:
        compress_img.workflow_compress_imgs(gitbook_path)
    # 生成SUMMARY.md和README.md
    generate_structured_md.workflow_generate_structured_md(gitbook_path)
    # 清除空文件夹
    mio.remove_empty_folders(gitbook_path)
    global_logger.info("Execution successfully")


def __prebook_diff(
    reorganize_imgs: bool,
    download_imgs: bool,
    rename_imgs: bool,
    optimize_imgs: bool,
    log_to_file: bool,
):
    if log_to_file:
        mlogger.setup_console_file_logger()
    else:
        mlogger.setup_console_logger()
    from common.mlogger import global_logger

    global_logger.info("Executing for files different from last commit...")
    global_logger.info(f"Options:")
    global_logger.info(f"  Log to File: {log_to_file}")
    global_logger.info(f"  Reorganize Images: {reorganize_imgs}")
    global_logger.info(f"  Download Images: {download_imgs}")
    global_logger.info(f"  Rename Images: {rename_imgs}")
    global_logger.info(f"  Optimize Images: {optimize_imgs}")
    gitbook_path = os.getcwd()
    global_logger.debug(f"Gitbook Path:" + gitbook_path)
    git_status_file_list = mgit.get_git_status_files(gitbook_path)
    # {}会创建一个set
    changed_folder_list = {
        mio.get_filepath_from_pathall(file_path) for file_path in git_status_file_list
    }
    for changed_folder in changed_folder_list:
        # 修改md中的图片引用格式, 移动图片位置, 下载md图片
        if reorganize_imgs:
            reformat_imgs_in_md.workflow_reformat_imgs_in_md(
                gitbook_path,
                reorganize_imgs,
                download_imgs,
                rename_imgs,
            )
        # 压缩图片, 可选
        if optimize_imgs:
            compress_img.workflow_compress_imgs(changed_folder)
    # 生成SUMMARY.md和README.md
    generate_structured_md.workflow_generate_structured_md(gitbook_path)
    # 清除空文件夹
    mio.remove_empty_folders(gitbook_path)
    global_logger.info("Execution successfully")


def __add_argument_to_subparser(subparser):
    subparser.add_argument(
        "-dr",
        "--dont-reorganize-imgs",
        action="store_false",
        help="Reorganize local pictures",
    )
    subparser.add_argument(
        "-d", "--download-imgs", action="store_true", help="Download web pictures"
    )
    subparser.add_argument(
        "-dn", "--dont-rename-imgs", action="store_false", help="Download web pictures"
    )
    subparser.add_argument(
        "-o", "--optimize-imgs", action="store_true", help="Compress jpgs and pngs"
    )
    subparser.add_argument(
        "-l", "--log-to-file", action="store_true", help="Output log to a file"
    )


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

    __add_argument_to_subparser(parser_all)

    # 子命令: diff
    parser_diff = subparsers.add_parser(
        "diff", help="Execute for files differs from last commit"
    )
    __add_argument_to_subparser(parser_diff)

    # 解析并处理命令
    args = parser.parse_args()
    if args.details:
        print(DESCRIPTION)
    elif args.command == "all":
        __prebook_all(
            not args.dont_reorganize_imgs,
            args.download_imgs,
            not args.dont_rename_imgs,
            args.optimize_imgs,
            args.log_to_file,
        )
    elif args.command == "diff":
        __prebook_diff(
            not args.dont_reorganize_imgs,
            args.download_imgs,
            not args.dont_rename_imgs,
            args.optimize_imgs,
            args.log_to_file,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
