from dataclasses import dataclass
from typing import List
import mio


CONFIG_FILE = "//43.82.125.244/ChinaUX/.auto/config/projects.json"


class SERIAL:
    SAK = "Sakura"
    TRI = "Trinity"
    URO = "Uroborous"
    VAL = "Valhalla"
    AME = "Amaebi"
    BF = "Bluefin"


class PROJNAME:
    class UR:
        Q_Rel = "Uro-Rel-Q"

    class VH:
        Q_DEV = "Val-Dev-Q"
        Q_REL_27 = "Val-27.0-Q"
        Q_REL_28 = "Val-28.0-Q"
        Q_REL_28_1 = "Val-28.1-Q"
        S_DEV = "Val-Dev-S"

    class AM:
        S1_DEV = "Amaebi1.1-Dev"
        S1_REL_2 = "Amaebi1.1-OTA2"
        S1_REL_4 = "Amaebi1.1-OTA4"
        S2_DEV = "Amaebi2.0-Dev"
        S2_RC_412 = "Amaebi2.0-RC4.12"
        S2_RC_510 = "Amaebi2.0-RC5.10"
        S21_DEV = "Amaebi2.1-Dev"
        S3_DEV = "Amaebi3.0-Dev"

    class BF:
        S1_DEV = "Bluefin1.1-Dev"


class ANDROID:
    Q = "Q"
    S = "S"
    U = "U"


@dataclass
class Project:
    name: str
    is_ota: bool
    serial: str
    model: List[str]
    android: str
    mtk: int
    branch: str
    last_pkg: str
    fix_version_list: List[str]


PROJECT_LIST_GLOBAL = []


def get_project_list() -> List[Project]:
    project_config_json = mio.get_json_from_file(file_all_path=CONFIG_FILE)
    if len(PROJECT_LIST_GLOBAL) != 0:
        return PROJECT_LIST_GLOBAL
    else:
        for project_name, project_info in project_config_json.items():
            project_item = None
            project_item = Project(
                name=project_name,
                is_ota=project_info["is_ota"],
                serial=project_info["serial"],
                model=project_info["model"],
                android=project_info["android"],
                mtk=project_info["mtk"],
                branch=project_info["branch"],
                last_pkg=project_info["last_pkg"],
                fix_version_list=project_info["fix_version_list"],
            )
            PROJECT_LIST_GLOBAL.append(project_item)
        return PROJECT_LIST_GLOBAL
