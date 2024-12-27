import requests

import os


def download_image(url, file_path_all):
    """
    Download image from network and save to local path
    :param url: The URL of the image
    :param file_path_all: The local file path to save the image
    """
    from common.mlogger import global_logger

    global_logger.debug(f"[download_image] Start download img from: {url}")
    try:
        # Ensure the directory exists
        folder_path = os.path.dirname(file_path_all)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            global_logger.debug(f"Target folder created: {folder_path}")

        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise exception for HTTP errors
        with open(file_path_all, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        global_logger.debug(f"Image successfully downloaded: {file_path_all}")
    except requests.RequestException as req_err:
        global_logger.error(f"Network error downloading image: {req_err}")
    except IOError as io_err:
        global_logger.error(f"File I/O error: {io_err}")
    except Exception as e:
        global_logger.error(f"Unexpected error downloading image: {e}")
