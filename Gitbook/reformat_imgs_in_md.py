from mlogger import global_logger

import os
import re

import mio
import mnet
import mstr
import mlogger
import minput

IMG_FORMAT = r"!\[.*?\]\((.*?)\)"
ROOT_DIR = mio.get_basename(mlogger.get_cwd())


def __find_image_references_in_md(md_data):
    matches = re.findall(IMG_FORMAT, md_data)
    return matches


def __is_drive_on_path(file_path: str) -> bool:
    if ":" in file_path:
        return True


def __is_root_on_path(file_path: str) -> bool:
    if ROOT_DIR in file_path:
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
    # 复制图片
    mio.copy_files(
        from_folder_path=img_folder_abs,
        from_file_name_or_format=img_file_name,
        to_folder_path=target_folder_abs,
        to_file_name=target_file_name,
    )
    # 删除图片
    mio.move_to_recycle_bin(mio.join_file_path(img_folder_abs, img_file_name))
    # 修改md中的引用
    md_data = md_data.replace(
        img_ref, os.path.join(target_folder_rel, target_file_name)
    )
    mio.write_data_to_file(file_all_path=md_file_path_all, data=md_data)
    minput.exit_or_continue()
    __reformat_imgs_in_md(md_file_path_all)
    return True


def __reformat_imgs_in_md(md_file_path_all):
    global_logger.debug(f">>> found md file: {md_file_path_all}")
    md_file_name = mio.get_filename_from_pathall(md_file_path_all)
    md_folder_abs = mio.get_filepath_from_pathall(md_file_path_all)
    md_data = mio.read_data_from_file(file_all_path=md_file_path_all)
    # 找到md文件中所有的imgs链接, 为防止md中引用了同一图片的情况, 每次修改图片后应该更新md文件, 并重新检索其中的img_refs
    img_ref_list = __find_image_references_in_md(md_data)
    for img_ref in img_ref_list:
        global_logger.debug(f">>> found img ref: {img_ref}")
        img_file_name = mio.get_filename_from_pathall(img_ref)
        img_folder_rel = mio.get_filepath_from_pathall(img_ref)
        img_folder_abs = mio.join_file_path(md_folder_abs, img_folder_rel)
        target_file_name = mstr.generate_random_alphanumeric() + mio.get_extension(
            img_file_name
        )
        target_folder_rel = mio.get_basename(md_file_name) + "_imgs"
        target_folder_abs = mio.join_file_path(md_folder_abs, target_folder_rel)

        if __is_weblink_on_name(img_ref):
            global_logger.warning(f"1. 网络图片需要下载, img_link: {img_ref}")
            mnet.download_image(
                img_ref,
                mio.join_file_path(target_folder_abs, target_file_name),
            )
            img_folder_abs = target_folder_abs
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
            break

        elif __is_drive_on_path(img_folder_rel) or __is_root_on_path(img_folder_rel):
            global_logger.warning(f"2. 盘符或仓库名称在图片引用路径中")
            # 先找下图片文件夹里有不啦
            found_img_list = mio.find_files_nc(
                file_path=img_folder_abs, file_name=img_file_name
            )
            if len(found_img_list) == 1:
                global_logger.debug(f"2-1. 在img文件夹内已找到文件, 将开始复制与删除")
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
                break
            else:
                # 再找下md同级目录或其子目录下
                found_img_list = mio.find_files(
                    file_path=md_folder_abs, file_name=img_file_name
                )
                if len(found_img_list) == 1:
                    global_logger.debug(
                        f"1-2. 在md文件夹内已找到文件, 将开始复制与删除"
                    )
                    img_folder_abs = mio.get_filepath_from_pathall(found_img_list[0])
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
                    break
                else:
                    global_logger.error(f"未找到图片!")

        elif target_folder_rel != img_folder_rel:
            global_logger.warning(
                f"3. 图片没有保存在正确格式的文件夹中, img_folder_rel: {img_folder_rel}, target_folder_rel: {target_folder_rel}"
            )
            # 按img_refs写的位置找下
            found_img_list = mio.find_files_nc(
                file_path=img_folder_abs, file_name=img_file_name
            )
            if found_img_list and len(found_img_list) == 1:
                global_logger.debug(f"3-1. 从img_refs已找到文件, 将开始复制与删除")
                img_folder_abs = mio.get_filepath_from_pathall(found_img_list[0])
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
                break
            else:
                # 再找下md同级目录或其子目录下
                found_img_list = mio.find_files(
                    file_path=md_folder_abs, file_name=img_file_name
                )
                if len(found_img_list) == 1:
                    global_logger.debug(
                        f"3-2. 在md文件夹内已找到文件, 将开始复制与删除"
                    )
                    img_folder_abs = mio.get_filepath_from_pathall(found_img_list[0])
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
                    break
                else:
                    global_logger.error(f"未找到图片!")

        elif not mstr.is_valid_alphanumeric(img_file_name):
            global_logger.warning(
                f"4. 图片名称不是11位字母和数字的组合, img_file_name: {img_file_name}"
            )
            found_img_list = mio.find_files_nc(
                file_path=img_folder_abs, file_name=img_file_name
            )
            global_logger.debug(f">>> found img list {found_img_list}")
            if len(found_img_list) == 1:
                global_logger.debug(f"4-1. 已找到文件, 将开始复制与删除")
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
                break
            else:
                global_logger.error(f"未找到图片!")


def workflow_reformat_imgs_in_md(file_path):
    global_logger.debug(
        "-----------------------workflow_reformat_imgs_in_md-----------------------"
    )
    # 找到所有的md文件
    md_file_list = mio.find_files(file_path=file_path, file_name=".md")
    for md_file_path_all in md_file_list:
        md_file_base_name = mio.get_basename(md_file_path_all)
        if md_file_base_name not in ["README.md", "SUMMARY.md"]:
            __reformat_imgs_in_md(md_file_path_all)


if __name__ == "__main__":
    workflow_reformat_imgs_in_md(".")
    input("任意键退出")
