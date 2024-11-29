import os
import re
import mio
from mlogger import global_logger

IMG_FORMAT = r"!\[.*?\]\((.*?)\)"


def __find_image_references_in_md(md_data):
    matches = re.findall(IMG_FORMAT, md_data)
    return matches


def workflow_reformat_imgs_in_md(file_path):
    global_logger.debug(
        "-----------------------workflow_reformat_imgs_in_md-----------------------"
    )
    md_file_list = mio.find_files_nc(file_path=file_path, file_name=".md")

    for md_file_path_all in md_file_list:
        global_logger.debug(f"found md file: {md_file_path_all}")
        md_name = mio.get_filename_from_pathall(md_file_path_all).replace(".md", "")
        md_path = mio.get_filepath_from_pathall(md_file_path_all)
        md_data = mio.read_data_from_file(file_all_path=md_file_path_all)
        img_ref_list = __find_image_references_in_md(md_data)
        is_refs_changed = False
        for img_ref in img_ref_list:
            global_logger.debug(f"found img ref: {img_ref}")
            if md_name + "_imgs" == mio.get_filepath_from_pathall(img_ref):
                global_logger.debug("图片引用已经用了正确的格式")
            else:
                is_refs_changed = True
                global_logger.warning("图片引用没有使用正确的格式")
                global_logger.debug("开始查找图片")
                img_file_name = mio.get_filename_from_pathall(img_ref)
                if "http" in img_ref:
                    global_logger.error("网络图片，去下载另存")
                elif "CSLibrary" in img_ref:
                    relative_path = split_path_after_keyword(img_ref, "CSLibrary")
                    global_logger.debug(f"绝对路径: {relative_path}")
                elif "CSGitbook" in img_ref:
                    relative_path = split_path_after_keyword(img_ref, "CSGitbook")
                    global_logger.debug(f"绝对路径: {relative_path}")
                else:
                    relative_path = os.path.join(md_path, img_file_name)
                    global_logger.debug(f"相对路径: {relative_path}")

                correct_absolute_path = os.path.join(LIB_PATH, relative_path)
                img_path = get_filepath_from_pathall(correct_absolute_path)
                img_name = get_filename_from_pathall(correct_absolute_path)
                found_img_list = find_files(file_path=img_path, file_name=img_name)
                global_logger.debug(f"found img list {found_img_list}")
                if len(found_img_list) == 0:
                    global_logger.warning("绝对路径找不到图片, 转为按文件名查找")
                    # 有个bug，(1).jpg这种格式只能识别到(1
                    if "(" in img_file_name:
                        global_logger.debug(f"转换图片: {img_file_name}")
                        found_img_list = find_files(
                            file_path=LIB_PATH, file_name=img_file_name + ").jpg"
                        )
                    else:
                        found_img_list = find_files(
                            file_path=LIB_PATH, file_name=img_file_name
                        )
                    if len(found_img_list) == 0:
                        global_logger.error("按文件名也找不到文件")
                    elif len(found_img_list) != 1:
                        global_logger.error("按文件名找到多张图片")
                elif len(found_img_list) != 1:
                    global_logger.error("找到多张图片")

                found_img_path_all = found_img_list[0]
                found_img_path = get_filepath_from_pathall(found_img_path_all)
                # 复制图片
                _, img_format = os.path.splitext(img_file_name)
                md_img_folder = os.path.join(md_path, md_name + "_imgs")
                global_logger.debug(f"img format: {img_format}")
                if found_img_path != md_img_folder:
                    global_logger.debug(f"img文件路径不一致，开始复制")
                    # 有个bug，(1).jpg这种格式只能识别到(1
                    if "(" in img_file_name:
                        # 复制图片
                        copy_files(
                            from_folder_path=found_img_path,
                            from_file_name_or_format=img_file_name + ").jpg",
                            to_folder_path=md_img_folder,
                            to_file_name=img_file_name + ").jpg",
                        )
                        # 删除图片
                        delete_files(
                            file_path=found_img_path, file_name_or_format=img_file_name
                        )
                    elif img_format:
                        # 复制图片
                        copy_files(
                            from_folder_path=found_img_path,
                            from_file_name_or_format=img_file_name,
                            to_folder_path=md_img_folder,
                            to_file_name=img_file_name,
                        )
                        # 删除图片
                        delete_files(
                            file_path=found_img_path, file_name_or_format=img_file_name
                        )
                    else:
                        # 复制图片
                        copy_files(
                            from_folder_path=found_img_path,
                            from_file_name_or_format=img_file_name,
                            to_folder_path=md_img_folder,
                            to_file_name=img_file_name + ".png",
                        )
                        # 删除图片
                        delete_files(
                            file_path=found_img_path, file_name_or_format=img_file_name
                        )
                        img_file_name = img_file_name + ".png"
                        exit_or_continue()
                else:
                    global_logger.debug(f"img文件路径一致")
                    exit_or_continue()
                # 修改md中的引用
                md_data = md_data.replace(
                    img_ref, os.path.join(md_name + "_imgs", img_file_name)
                )
        if is_refs_changed:
            global_logger.debug(f"修改md文件中的引用{md_file_path_all}")
            write_data_to_file(file_all_path=md_file_path_all, data=md_data)
            exit_or_continue()


def split_path_after_keyword(path, keyword):
    parts = path.split(keyword, 1)
    if len(parts) > 1:
        splited_path = parts[1].lstrip(os.path.sep)
        return splited_path
    else:
        return None


if __name__ == "__main__":
    md_file_list = get_md_file_list()
    img_to_folder(md_file_list)
    input("任意键退出")
