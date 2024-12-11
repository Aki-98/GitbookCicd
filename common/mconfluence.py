from mauth import CONFLUENCE_TOKEN

from mlogger import global_logger

import requests

API_CREATE = "https://csc-jira.sony.com.cn:8443/rest/api/content"
API_PAGE = "https://csc-jira.sony.com.cn:8443/rest/api/content/{page_id}"
API_PAGE_EXPAND_BODY = (
    "https://csc-jira.sony.com.cn:8443/rest/api/content/{page_id}?expand=body.storage"
)
API_HEADERS = {
    "Authorization": f"Bearer {CONFLUENCE_TOKEN}",
    "Content-Type": "application/json",
}
SPACE_KEY = "TC"


def create_page(page_data: dict):
    response = requests.post(API_CREATE, headers=API_HEADERS, json=page_data)
    if response.status_code == 200:
        global_logger.debug(f"Page created successfully.")
        page_id = response.json()["id"]
        global_logger.debug(f"Page id:{page_id}")
        return page_id
    else:
        global_logger.warning(f"Page created failed.")
        global_logger.warning(f"code:{response.status_code}")
        global_logger.warning(f"reason:{response.reason}")


def get_page(page_id: str):
    page_url = API_PAGE.format(page_id=page_id)
    response = requests.get(page_url, headers=API_HEADERS)
    if response.status_code == 200:
        global_logger.debug(f"Page get successfully.")
        return response.json()
    else:
        global_logger.warning(f"Page get failed.")
        global_logger.warning(f"code:{response.status_code}")
        global_logger.warning(f"reason:{response.reason}")


def get_page_expand_body(page_id: str):
    page_url = API_PAGE_EXPAND_BODY.format(page_id=page_id)
    response = requests.get(page_url, headers=API_HEADERS)
    if response.status_code == 200:
        global_logger.debug(f"Page get expand body successfully.")
        return response.json()
    else:
        global_logger.warning(f"Page get expand bodyfailed.")
        global_logger.warning(f"code:{response.status_code}")
        global_logger.warning(f"reason:{response.reason}")


def update_page(page_id: str, update_data: dict):
    page_url = API_PAGE.format(page_id=page_id)
    response = requests.put(page_url, headers=API_HEADERS, json=update_data)
    if response.status_code == 200:
        global_logger.debug(f"Page put successfully.")
        return response.json()
    else:
        global_logger.warning(f"Page put failed.")
        global_logger.warning(f"code:{response.status_code}")
        global_logger.warning(f"reason:{response.reason}")


def get_page_html(page_id: str):
    page_data = get_page_expand_body(page_id)
    return page_data["body"]["storage"]["value"]


def get_html_by_content(page_data: dict):
    return page_data["body"]["storage"]["value"]


def arrange_update_page_data(page_data: dict, html: str, title: str = None):
    new_page_data = {
        "id": page_data["id"],
        "type": "page",
        "title": page_data["title"] if not title else title,
        "version": {"number": page_data["version"]["number"] + 1},
        "body": {
            "storage": {
                "value": html,
                "representation": "storage",
            }
        },
    }
    return new_page_data


def arrange_create_page_data(parent_page_id: str, page_title: str, page_html: str):
    page_data = {
        "type": "page",
        "title": page_title,
        "ancestors": [{"id": parent_page_id}],
        "space": {"key": SPACE_KEY},
        "body": {"storage": {"value": page_html, "representation": "storage"}},
    }
    return page_data
