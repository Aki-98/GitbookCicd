from mlogger import global_logger

import os
import re

import mio
import mnet
import mstr
import mlogger

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
    target_img_file_path_relative,
    target_img_file_name,
    target_img_path_abs,
    img_file_name,
    img_file_path_abs,
    img_ref,
    md_data,
):
    global_logger.debug(f"__reformat_img with img_file_path_abs: {img_file_path_abs}")
    # 复制图片
    mio.copy_files(
        from_folder_path=img_file_path_abs,
        from_file_name_or_format=img_file_name,
        to_folder_path=target_img_path_abs,
        to_file_name=target_img_file_name,
    )
    # 删除图片
    mio.move_to_recycle_bin(mio.join_file_path(img_file_path_abs, img_file_name))
    # 修改md中的引用
    md_data = md_data.replace(
        img_ref, os.path.join(target_img_file_path_relative, target_img_file_name)
    )
    return True, md_data


def workflow_reformat_imgs_in_md(file_path):
    global_logger.debug(
        "-----------------------workflow_reformat_imgs_in_md-----------------------"
    )
    # 找到所有的md文件
    md_file_list = mio.find_files_nc(file_path=file_path, file_name=".md")
    for md_file_path_all in md_file_list:
        global_logger.debug(f">>> found md file: {md_file_path_all}")
        # md文件名称
        md_file_name = mio.get_filename_from_pathall(md_file_path_all)
        # md文件的绝对路径
        md_file_path_abs = mio.get_filepath_from_pathall(md_file_path_all)
        # md文件的内容
        md_data = mio.read_data_from_file(file_all_path=md_file_path_all)
        # 找到md文件中所有的imgs链接
        img_ref_list = __find_image_references_in_md(md_data)
        is_refs_changed = False
        for img_ref in img_ref_list:
            global_logger.debug(f">>> found img ref: {img_ref}")
            # 从img_ref提取出img文件的相对路径(除开文件名的部分)
            img_file_path_rel = mio.get_filepath_from_pathall(img_ref)
            # 从img_ref提取出img文件名称
            img_file_name = mio.get_filename_from_pathall(img_ref)
            # 后续每次格式化前应该都先找到正确的img_path_abs
            img_path_abs = ""
            # 应修改成的, img文件存放的文件夹
            target_img_file_path_rel = mio.get_basename(md_file_name) + "_imgs"
            # 应修改成的, img文件的名称
            target_img_file_name = (
                mstr.generate_random_alphanumeric() + mio.get_extension(img_file_name)
            )
            # 应重新放置的, img文件存放绝对路径
            target_img_path_abs = mio.join_file_path(
                md_file_path_abs, target_img_file_path_rel
            )

            if __is_drive_on_path(img_file_path_rel):
                global_logger.warning(f"1. 盘符在图片引用路径中")
                # 可能路径由本机保存
                found_img_list = mio.find_files_nc(
                    file_path=img_file_path_rel, file_name=img_file_name
                )
                global_logger.debug(f">>> found img list {found_img_list}")
                if len(found_img_list) == 1:
                    global_logger.debug(
                        f"1-1. 图片由本机保存, 已找到文件, 将开始复制与删除"
                    )
                    img_file_path_abs = img_ref
                    is_refs_changed, md_data = __reformat_img(
                        target_img_file_path_rel,
                        target_img_file_name,
                        target_img_path_abs,
                        img_file_name,
                        img_file_path_abs,
                        img_ref,
                        md_data,
                    )
                    continue
                else:
                    # 可能路径由其他机器保存，但图片至少应该放置在md同级目录或其子目录下
                    found_img_list = mio.find_files(
                        file_path=md_file_path_abs, file_name=img_file_name
                    )
                    global_logger.debug(f">>> found img list {found_img_list}")
                    if len(found_img_list) == 1:
                        global_logger.debug(
                            f"1-2. 图片由其他机器保存, 已找到文件, 将开始复制与删除"
                        )
                        img_path_abs = found_img_list[0]
                        is_refs_changed, md_data = __reformat_img(
                            target_img_file_path_rel,
                            target_img_file_name,
                            target_img_path_abs,
                            img_file_name,
                            img_file_path_abs,
                            img_ref,
                            md_data,
                        )
                        continue
                    else:
                        global_logger.error(f"未找到图片!")

            if __is_root_on_path(img_file_path_rel):
                global_logger.warning(f"2. 根文件夹名称在图片引用路径中")
                # 图片至少应该放置在md同级目录或其子目录下
                found_img_list = mio.find_files(
                    file_path=md_file_path_abs, file_name=img_file_name
                )
                global_logger.debug(f">>> found img list {found_img_list}")
                if len(found_img_list) == 1:
                    global_logger.debug(f"2-1. 已找到文件, 将开始复制与删除")
                    img_path_abs = found_img_list[0]
                    is_refs_changed, md_data = __reformat_img(
                        target_img_file_path_rel,
                        target_img_file_name,
                        target_img_path_abs,
                        img_file_name,
                        img_file_path_abs,
                        img_ref,
                        md_data,
                    )
                    continue
                else:
                    global_logger.error(f"未找到图片!")

            if __is_weblink_on_name(img_ref):
                global_logger.warning(f"3. 网络图片需要下载, img_link:{img_file_name}")
                mnet.download_image(
                    img_ref,
                    mio.join_file_path(target_img_path_abs, target_img_file_name),
                )
                img_path_abs = target_img_path_abs
                is_refs_changed, md_data = __reformat_img(
                    target_img_file_path_rel,
                    target_img_file_name,
                    target_img_path_abs,
                    img_file_name,
                    img_file_path_abs,
                    img_ref,
                    md_data,
                )
                continue

            if target_img_file_path_rel not in img_file_path_rel:
                global_logger.warning(
                    f"4. 图片没有保存在正确格式的文件夹中, img_file_path_relative:{img_file_path_rel}"
                )
                # 按img_refs写的位置找下
                img_path_abs = mio.join_file_path(md_file_path_abs, img_file_path_rel)
                found_img_list = mio.find_files_nc(
                    file_path=img_path_abs, file_name=img_file_name
                )
                global_logger.debug(f">>> found img list {found_img_list}")
                if len(found_img_list) == 1:
                    global_logger.debug(f"4-1. 已找到文件, 将开始复制与删除")
                    img_path_abs = found_img_list[0]
                    is_refs_changed, md_data = __reformat_img(
                        target_img_file_path_rel,
                        target_img_file_name,
                        target_img_path_abs,
                        img_file_name,
                        img_file_path_abs,
                        img_ref,
                        md_data,
                    )
                    continue
                else:
                    global_logger.error(f"未找到图片!")

            if not mstr.is_valid_alphanumeric(img_file_name):
                global_logger.warning(
                    f"4. 图片名称不是11位字母和数字的组合, img_file_name:{img_file_name}"
                )
                # 按img_refs写的位置找下
                img_path_abs = mio.join_file_path(md_file_path_abs, img_file_path_rel)
                found_img_list = mio.find_files_nc(
                    file_path=img_path_abs, file_name=img_file_name
                )
                global_logger.debug(f">>> found img list {found_img_list}")
                if len(found_img_list) == 1:
                    global_logger.debug(f"4-1. 已找到文件, 将开始复制与删除")
                    img_path_abs = found_img_list[0]
                    is_refs_changed, md_data = __reformat_img(
                        target_img_file_path_rel,
                        target_img_file_name,
                        target_img_path_abs,
                        img_file_name,
                        img_file_path_abs,
                        img_ref,
                        md_data,
                    )
                    continue
                else:
                    global_logger.error(f"未找到图片!")
        if is_refs_changed:
            global_logger.debug(
                f"md文件中的引用已经被修改, md_file_path_all: {md_file_path_all}"
            )
            mio.write_data_to_file(file_all_path=md_file_path_all, data=md_data)
    # 删除空文件夹
    mio.remove_empty_folders(file_path)


if __name__ == "__main__":
    workflow_reformat_imgs_in_md(".")
    input("任意键退出")
