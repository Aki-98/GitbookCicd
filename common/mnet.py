from common.mlogger import global_logger

import requests

from common import mio


def download_image(url, file_path_all):
    """
    Download image from network and save to local path
    :param url
    :param save_path
    """
    global_logger.debug(f"[download_image] Start download img from: {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        mio.create_folder_of_file_if_not_exist(file_path_all)
        with open(file_path_all, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        global_logger.debug(f"Image successfully downloaded: {file_path_all}")
    except Exception as e:
        global_logger.error(f"Error downloading image: {e}")
