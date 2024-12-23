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
    log_to_file: bool,
    reorganize_imgs: bool,
    download_imgs: bool,
    rename_imgs: bool,
    optimize_imgs: bool,
):
    if log_to_file:
        cli_logger = mlogger.global_logger
    else:
        cli_logger = mlogger.console_logger
    cli_logger.info("Executing for all files...")
    cli_logger.debug(f"Options:")
    cli_logger.debug(f"  Log to File: {log_to_file}")
    cli_logger.debug(f"  Reorganize Images: {reorganize_imgs}")
    cli_logger.debug(f"  Download Images: {download_imgs}")
    cli_logger.debug(f"  Rename Images: {rename_imgs}")
    cli_logger.debug(f"  Optimize Images: {optimize_imgs}")
    # gitbook_path = mio.join_file_path("E:\.personal\CSGitbook")
    gitbook_path = "E:\.personal\\temp"
    cli_logger.debug(f"Gitbook Path:" + gitbook_path)
    # 修改md中的图片引用格式, 移动图片位置, 下载md图片
    if reorganize_imgs:
        reformat_imgs_in_md.workflow_reformat_imgs_in_md(
            cli_logger, gitbook_path, download_imgs
        )
    # 压缩图片, 可选
    if optimize_imgs:
        compress_img.workflow_compress_imgs(cli_logger, gitbook_path)
    # 生成SUMMARY.md和README.md
    generate_structured_md.workflow_generate_structured_md(cli_logger, gitbook_path)
    # 清除空文件夹
    mio.remove_empty_folders(cli_logger, gitbook_path)
    cli_logger.info("Execution successfully")


def __prebook_diff(
    log_to_file: bool,
    reorganize_imgs: bool,
    download_imgs: bool,
    rename_imgs: bool,
    optimize_imgs: bool,
):
    if log_to_file:
        cli_logger = mlogger.global_logger
    else:
        cli_logger = mlogger.console_logger
    cli_logger.info("Executing for files different from last commit...")
    cli_logger.debug(f"Options:")
    cli_logger.debug(f"  Log to File: {log_to_file}")
    cli_logger.debug(f"  Reorganize Images: {reorganize_imgs}")
    cli_logger.debug(f"  Download Images: {download_imgs}")
    cli_logger.debug(f"  Rename Images: {rename_imgs}")
    cli_logger.debug(f"  Optimize Images: {optimize_imgs}")
    gitbook_path = os.getcwd()
    cli_logger.debug(f"Gitbook Path:" + gitbook_path)
    git_status_file_list = mgit.get_git_status_files(cli_logger, gitbook_path)
    # {}会创建一个set
    changed_folder_list = {
        mio.get_filepath_from_pathall(file_path) for file_path in git_status_file_list
    }
    for changed_folder in changed_folder_list:
        # 修改md中的图片引用格式, 移动图片位置, 下载md图片
        if reorganize_imgs:
            reformat_imgs_in_md.workflow_reformat_imgs_in_md(
                cli_logger, changed_folder, download_imgs
            )
        # 压缩图片, 可选
        if optimize_imgs:
            compress_img.workflow_compress_imgs(cli_logger, changed_folder)
    # 生成SUMMARY.md和README.md
    generate_structured_md.workflow_generate_structured_md(cli_logger, gitbook_path)
    # 清除空文件夹
    mio.remove_empty_folders(cli_logger, gitbook_path)
    cli_logger.info("Execution successfully")


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
        "-dr",
        "--dont-reorganize-imgs",
        action="store_false",
        help="Reorganize local pictures",
    )
    parser.add_argument(
        "-d", "--download-imgs", action="store_true", help="Download web pictures"
    )
    parser.add_argument(
        "-dn", "--dont-rename-imgs", action="store_false", help="Download web pictures"
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
