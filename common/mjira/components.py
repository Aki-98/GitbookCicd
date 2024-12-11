import mgerrit.provider
from mgerrit.config import SERIAL, Project

import mjira.components
from mlogger import global_logger

import mstr
import mio

import mjira.const
import mgerrit.config
import mmodule.provider

CONFIG_FILE = "//43.82.125.244/ChinaUX/.auto/config/sync_keywords.json"

PROJECT_LIST = mgerrit.config.get_project_list()


class COMPONENT_PROJECT:
    URO_Q = "UroQ"
    URO_S = "UroS"
    VH2_DV = "Val2.2DV"
    VH2_OTA = "Val2.2OTA"
    AE1_DV = "Amaebi1.0DV"
    AE1_OTA = "Amaebi1.1OTA"
    AE2_DV = "Amaebi2.0DV"
    AE2_OTA = "Amaebi2.0OTA"
    AE21_DV = "Amaebi2.1DV"
    VAL_S = "ValS"
    T6Y = "T6Y"


# Unified fixversion to lowercase
class FIX_VERSION_EXTERNAL:
    QUAILTY_MONITORING = "QualityMonitoring"
    TRD_PARTY_MONITORING = "3rd Party Monitoring"
    REGULATION_20 = "Regulation2.0"


class COMPONENT_MODULE:
    MYSONY = "MySony"
    SEARCH_APP = "VoiceAssistant"
    MOBILE_CONNECTIVITY = "MobileConnectivity"
    WECHAT_SHARING = "WechatSharing"
    VIDEO_CHAT = "VideoChat"
    KIDS_ADAPTER = "KidsElder"
    CHINA_HOME = "ChinaHome"
    IOT = "IoT"
    CONTROL_PROXY = "Control Proxy"
    ACCOUNT_APP = "AccountApp"
    APP_ASSISTANT = "AppAssistant"
    BRAVIA_SHOW = "BraviaShow"
    PARTNER_KEY = "PartnerKey"
    OTHERS = "Others"
    CHERRY = "CherryTask"


class FIX_VERSION_DQA_TASK:
    URO_Q = "Uroboros-Q-Main"
    VH_Q_DV = "Valhalla-Q-Main"
    VH_Q_23 = "Valhalla-Q-23.0"
    VH_S_DV = "Valhalla-S-DV"
    AE2_DV = "Amaebi2.0-DV"
    AE2_OTA = "Amaebi2.0-OTA"
    AE1_DV = "Amaebi1.1-DV"
    AE1_OTA = "Amaebi1.1-OTA"


COMPONENT_MODULE_LIST = [
    getattr(COMPONENT_MODULE, attr)
    for attr in dir(COMPONENT_MODULE)
    if not callable(getattr(COMPONENT_MODULE, attr)) and not attr.startswith("__")
]

# --------------------CSC Model -------------------

SYNC_KEYWORDS_DICT = mio.get_json_from_file(file_all_path=CONFIG_FILE)


def detect_csc_model_component_by_summary(summary: str) -> str:
    """Determine which application the BUG belongs to by some keywords."""
    summary = summary.lower()
    for component_name, keyword_list in SYNC_KEYWORDS_DICT.items():
        if mstr.check_str_in_array(summary, keyword_list):
            return component_name
    return COMPONENT_MODULE.OTHERS


def remove_csc_model_component_list(component_list: list) -> list:
    component_list_removed = []
    for component in component_list:
        if component not in mmodule.provider.get_module_component_list():
            component_list_removed.append(component)
    return component_list_removed


def get_csc_model_component_list(component_list: list) -> list:
    component_list_is_app = []
    for component in component_list:
        if component in COMPONENT_MODULE_LIST:
            component_list_is_app.append(component)
    return component_list_is_app


# --------------------DQA Task -------------------


def get_dqa_test_project_component(project: Project):
    serial = project.serial
    android = project.android
    if serial == SERIAL.URO and android == "Q":
        return mjira.components.FIX_VERSION_DQA_TASK.URO_Q
    if serial == SERIAL.VAL and android == "Q":
        return mjira.components.FIX_VERSION_DQA_TASK.VH_Q_DV
    if serial == SERIAL.VAL and android == "S":
        return mjira.components.FIX_VERSION_DQA_TASK.VH_S_DV
    if serial == SERIAL.AME and android == "S":
        return mjira.components.FIX_VERSION_DQA_TASK.AE2_OTA
    global_logger.warning(f"Component related to project id {project.name} not found")
