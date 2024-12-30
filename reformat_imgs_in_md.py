import os
import re

from common import mio
from common import mnet
from common import mstr

IMG_FORMAT = r"!\[.*?\]\((.*?)\)"
GITBOOK_REPO_NAME: str = ""


def __find_image_references_in_md(md_data):
    matches = re.findall(IMG_FORMAT, md_data)
    return matches


def __is_drive_on_path(file_path: str) -> bool:
    if ":" in file_path:
        return True


def __is_root_on_path(file_path: str) -> bool:
    if GITBOOK_REPO_NAME in file_path:
        return True


def __is_weblink_on_name(file_name: str) -> bool:
    if mstr.extract_web_link_list(file_name):
        return True


def __reformat_img(
    img_ref,
    img_folder_abs,
    img_file_name,
    target_folder_rel,
    target_folder_abs,
    target_file_name,
    md_file_path_all,
    md_data,
):
    global_logger.debug(f"__reformat_img with img_folder_abs: {img_folder_abs}")
    if img_file_name == target_file_name and img_folder_abs == target_folder_abs:
        global_logger.debug(
            f"img file name and folder compact with the target, no need to replace"
        )
    else:
        # Copy the image
        mio.copy_files(
            from_folder_path=img_folder_abs,
            from_file_name_or_format=img_file_name,
            to_folder_path=target_folder_abs,
            to_file_name=target_file_name,
        )
        # Delete the image
        mio.move_to_recycle_bin(mio.join_file_path(img_folder_abs, img_file_name))
    # Update the image reference in the markdown file
    md_data = md_data.replace(
        img_ref, os.path.join(target_folder_rel, target_file_name)
    )
    mio.write_data_to_file(file_all_path=md_file_path_all, data=md_data)
    return True


def __reformat_imgs_in_md(md_file_path_all: str):
    global_logger.debug(f">>> Found markdown file: {md_file_path_all}")
    md_file_name = mio.get_filename_from_pathall(md_file_path_all)
    md_folder_abs = mio.get_filepath_from_pathall(md_file_path_all)
    md_data = mio.read_data_from_file(file_all_path=md_file_path_all)
    # Find all image links in the markdown file.
    # To prevent modifying the same image reference multiple times, the markdown file should be updated and re-scanned after each modification.
    img_ref_list = __find_image_references_in_md(md_data)
    for img_ref in img_ref_list:
        global_logger.debug(f">> Found image reference: {img_ref}")
        img_file_name = mio.get_filename_from_pathall(img_ref)
        img_folder_rel = mio.get_filepath_from_pathall(img_ref)
        img_folder_abs = mio.join_file_path(md_folder_abs, img_folder_rel)
        target_file_name = (
            mstr.generate_random_alphanumeric() + mio.get_extension(img_file_name)
            if RENAME_IMGS
            else img_file_name
        )
        target_folder_rel = (
            mio.get_basename(md_file_name) + "_imgs"
            if REORGANIZE_IMGS or DOWNLOAD_IMGS
            else img_folder_rel
        )
        target_folder_abs = mio.join_file_path(md_folder_abs, target_folder_rel)
        if DOWNLOAD_IMGS and __is_weblink_on_name(img_ref):
            global_logger.info(
                f"1. Network image needs to be downloaded, img_link: {img_ref}"
            )
            mnet.download_image(
                img_ref,
                mio.join_file_path(target_folder_abs, target_file_name),
            )
            # 下载时就已经重命名并放置在响应文件夹下了
            img_folder_abs = target_folder_abs
            img_file_name = target_file_name
            __reformat_img(
                img_ref,
                img_folder_abs,
                img_file_name,
                target_folder_rel,
                target_folder_abs,
                target_file_name,
                md_file_path_all,
                md_data,
            )
            __reformat_imgs_in_md(md_file_path_all)
            break

        elif REORGANIZE_IMGS and (
            __is_drive_on_path(img_folder_rel) or __is_root_on_path(img_folder_rel)
        ):
            global_logger.info(
                f"2. Drive or repository name found in the image reference path."
            )
            # Check if the image exists in the specified folder
            found_img_list = mio.find_files_nc(
                file_path=img_folder_abs, file_name=img_file_name
            )
            if len(found_img_list) == 1:
                global_logger.debug(
                    f"2-1. File found in the image folder, proceeding to copy and delete."
                )
                __reformat_img(
                    img_ref,
                    img_folder_abs,
                    img_file_name,
                    target_folder_rel,
                    target_folder_abs,
                    target_file_name,
                    md_file_path_all,
                    md_data,
                )
                __reformat_imgs_in_md(md_file_path_all)
                break
            else:
                # Check in the markdown's directory or its subdirectories
                found_img_list = mio.find_files(
                    file_path=md_folder_abs, file_name=img_file_name
                )
                if len(found_img_list) == 1:
                    global_logger.debug(
                        f"1-2. File found in the markdown directory, proceeding to copy and delete."
                    )
                    img_folder_abs = mio.resolve_relative_path(
                        mio.get_filepath_from_pathall(found_img_list[0])
                    )
                    __reformat_img(
                        img_ref,
                        img_folder_abs,
                        img_file_name,
                        target_folder_rel,
                        target_folder_abs,
                        target_file_name,
                        md_file_path_all,
                        md_data,
                    )
                    __reformat_imgs_in_md(md_file_path_all)
                    break
                else:
                    global_logger.error(f"Image not found!")

        elif REORGANIZE_IMGS and (
            target_folder_rel != img_folder_rel
        ):  # 没有()运算顺序也是正确的
            global_logger.info(
                f"3. Image not saved in the correct folder, img_folder_rel: {img_folder_rel}, target_folder_rel: {target_folder_rel}"
            )
            # Try locating the image using the reference in the markdown file
            found_img_list = mio.find_files_nc(
                file_path=img_folder_abs, file_name=img_file_name
            )
            if found_img_list and len(found_img_list) == 1:
                global_logger.debug(
                    f"3-1. File found via image reference, proceeding to copy and delete."
                )
                img_folder_abs = mio.resolve_relative_path(
                    mio.get_filepath_from_pathall(found_img_list[0])
                )
                __reformat_img(
                    img_ref,
                    img_folder_abs,
                    img_file_name,
                    target_folder_rel,
                    target_folder_abs,
                    target_file_name,
                    md_file_path_all,
                    md_data,
                )
                __reformat_imgs_in_md(md_file_path_all)
                break
            else:
                # Check in the markdown's directory or its subdirectories
                found_img_list = mio.find_files(
                    file_path=md_folder_abs, file_name=img_file_name
                )
                if len(found_img_list) == 1:
                    global_logger.debug(
                        f"3-2. File found in the markdown directory, proceeding to copy and delete."
                    )
                    img_folder_abs = mio.resolve_relative_path(
                        mio.get_filepath_from_pathall(found_img_list[0])
                    )
                    __reformat_img(
                        img_ref,
                        img_folder_abs,
                        img_file_name,
                        target_folder_rel,
                        target_folder_abs,
                        target_file_name,
                        md_file_path_all,
                        md_data,
                    )
                    __reformat_imgs_in_md(md_file_path_all)
                    break
                else:
                    global_logger.error(f"Image not found!")

        elif RENAME_IMGS and not mstr.is_valid_alphanumeric(img_file_name):
            global_logger.info(
                f"4. Image name is not a valid 11-character alphanumeric string, img_file_name: {img_file_name}"
            )
            found_img_list = mio.find_files_nc(
                file_path=img_folder_abs, file_name=img_file_name
            )
            global_logger.debug(f">>> Found image list {found_img_list}")
            if len(found_img_list) == 1:
                global_logger.debug(f"4-1. File found, proceeding to copy and delete.")
                __reformat_img(
                    img_ref,
                    img_folder_abs,
                    img_file_name,
                    target_folder_rel,
                    target_folder_abs,
                    target_file_name,
                    md_file_path_all,
                    md_data,
                )
                __reformat_imgs_in_md(md_file_path_all)
                break
            else:
                global_logger.error(f"Image not found!")


def workflow_reformat_imgs_in_md(
    booklib_path: str,
    reorganize_imgs: bool,
    download_imgs: bool,
    rename_imgs: bool,
):
    global global_logger
    from common.mlogger import global_logger

    global_logger.info("\nStart reformatting images in markdown...")
    global GITBOOK_REPO_NAME
    GITBOOK_REPO_NAME = mio.get_basename(booklib_path)

    global REORGANIZE_IMGS
    REORGANIZE_IMGS = reorganize_imgs
    global DOWNLOAD_IMGS
    DOWNLOAD_IMGS = download_imgs
    global RENAME_IMGS
    RENAME_IMGS = rename_imgs

    # Find all markdown files
    md_file_list = mio.find_files(file_path=booklib_path, file_name=".md")

    for md_file_path_all in md_file_list:
        md_file_base_name = mio.get_basename(md_file_path_all)
        if md_file_base_name not in ["README.md", "SUMMARY.md"]:
            __reformat_imgs_in_md(md_file_path_all)
