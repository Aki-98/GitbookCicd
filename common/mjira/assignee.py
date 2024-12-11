from dataclasses import dataclass

from mlogger import global_logger
from typing import List

import mio

CONFIG_FILE = "//43.82.125.244/ChinaUX/.auto/config/jira_users.json"


@dataclass
class Assignee:
    name_en: str
    name_cn: str
    guid: str


class ASSIGNEE_NAME:
    CHERRY = "yanjing.wu"
    BINYU = "binyu.ren"
    BANGO = "bangguo.wang"
    QING = "qingqiu.li"
    NIU = "jiajun.niu"
    ZHEBIN = "zhebin.zhang"
    BICHENG = "bicheng.zhang"
    CAOCAN = "can.cao"
    LIWEI = "liwei.wang"
    ZIYAO = "ziyao.zhou"
    YIWEI = "yiwei.wang"
    LAI = "zewen.lai"
    FENG_JING_CHAO = "jingchao.feng"
    FRANK = "zijin.hu"


ASSIGNEE_CHINAUX_DEVELOPER: List[Assignee] = []
ASSIGNEE_CHINAUX_LEADER: List[Assignee] = []
ASSIGNEE_CHINAUX_RELEATED: List[Assignee] = []
ASSIGNEE_OTHERS: List[Assignee] = []


def __init_assignee_list():
    assignee_config_json = mio.get_json_from_file(file_all_path=CONFIG_FILE)
    for assignee_info in assignee_config_json["cnux_developer"]:
        assignee_item = None
        assignee_item = Assignee(
            name_en=assignee_info["name_en"],
            name_cn=assignee_info["name_cn"],
            guid=assignee_info["guid"],
        )
        ASSIGNEE_CHINAUX_DEVELOPER.append(assignee_item)
    for assignee_info in assignee_config_json["cnux_leader"]:
        assignee_item = None
        assignee_item = Assignee(
            name_en=assignee_info["name_en"],
            name_cn=assignee_info["name_cn"],
            guid=assignee_info["guid"],
        )
        ASSIGNEE_CHINAUX_LEADER.append(assignee_item)
    for assignee_info in assignee_config_json["cnux_related"]:
        assignee_item = None
        assignee_item = Assignee(
            name_en=assignee_info["name_en"],
            name_cn=assignee_info["name_cn"],
            guid=assignee_info["guid"],
        )
        ASSIGNEE_CHINAUX_RELEATED.append(assignee_item)
    for assignee_info in assignee_config_json["others"]:
        assignee_item = None
        assignee_item = Assignee(
            name_en=assignee_info["name_en"],
            name_cn=assignee_info["name_cn"],
            guid=assignee_info["guid"],
        )
        ASSIGNEE_OTHERS.append(assignee_item)


def get_assignee_cnux_developer_list() -> List[Assignee]:
    if len(ASSIGNEE_CHINAUX_DEVELOPER) == 0:
        __init_assignee_list()
    return ASSIGNEE_CHINAUX_DEVELOPER


def get_assignee_cnux_leader_list() -> List[Assignee]:
    if len(ASSIGNEE_CHINAUX_LEADER) == 0:
        __init_assignee_list()
    return ASSIGNEE_CHINAUX_LEADER


def get_assignee_cnux_related_list() -> List[Assignee]:
    if len(ASSIGNEE_CHINAUX_RELEATED) == 0:
        __init_assignee_list()
    return ASSIGNEE_CHINAUX_RELEATED


def get_assignee_cnux_others_list() -> List[Assignee]:
    if len(ASSIGNEE_OTHERS) == 0:
        __init_assignee_list()
    return ASSIGNEE_OTHERS


def is_assignee_in_chinaux(guid_or_username):
    for assignee in get_assignee_cnux_developer_list():
        if guid_or_username in [assignee.name_en, assignee.guid]:
            return True
    return False


def is_assignee_in_chinaux_should_handle(guid_or_username):
    for assignee in (
        get_assignee_cnux_developer_list() + get_assignee_cnux_leader_list()
    ):
        if guid_or_username in [assignee.name_en, assignee.guid]:
            return True
    return False


def get_username_en(compact_str: str) -> str:
    if compact_str:
        compact_str = compact_str.strip()
    if not compact_str:
        global_logger.error("compact_str is empty")
    for assignee in (
        get_assignee_cnux_developer_list()
        + get_assignee_cnux_leader_list()
        + get_assignee_cnux_related_list()
        + get_assignee_cnux_others_list()
    ):
        if (
            assignee.guid == compact_str
            or assignee.name_en == compact_str
            or assignee.name_cn == compact_str
        ):
            return assignee.name_en


def get_username_cn(compact_str: str) -> str:
    if compact_str:
        compact_str = compact_str.strip()
    if not compact_str:
        global_logger.error("compact_str is empty")
    for assignee in (
        get_assignee_cnux_developer_list()
        + get_assignee_cnux_leader_list()
        + get_assignee_cnux_related_list()
        + get_assignee_cnux_others_list()
    ):
        if (
            assignee.guid == compact_str
            or assignee.name_en == compact_str
            or assignee.name_cn == compact_str
        ):
            return assignee.name_cn


def get_guid(compact_str: str) -> str:
    if compact_str:
        compact_str = compact_str.strip()
    if not compact_str:
        global_logger.error("compact_str is empty")
    for assignee in (
        get_assignee_cnux_developer_list()
        + get_assignee_cnux_leader_list()
        + get_assignee_cnux_related_list()
        + get_assignee_cnux_others_list()
    ):
        if (
            assignee.guid == compact_str
            or assignee.name_en == compact_str
            or assignee.name_cn == compact_str
        ):
            return assignee.guid


def get_guid_list_of_cnux_should_handle() -> list:
    return [assignee.guid for assignee in get_assignee_cnux_developer_list()] + [
        assignee.guid for assignee in get_assignee_cnux_leader_list()
    ]


if __name__ == "__main__":
    __init_assignee_list()
