from const_jira import COMPONENT_MODEL, COMPONENT_FIX_VERSION
from const_repo import PROJECTS, SERIAL

from mlogger import global_logger

const_uro = [key for key, value in PROJECTS.items() if value.serial == SERIAL.URO]
const_vhq = [
    key
    for key, value in PROJECTS.items()
    if value.serial == SERIAL.VAL and value.android == "Q"
]
const_vhs = [
    key
    for key, value in PROJECTS.items()
    if value.serial == SERIAL.VAL and value.android == "S"
]
const_ae1 = [
    key
    for key, value in PROJECTS.items()
    if value.serial == SERIAL.AME and "1" in value.model
]
const_ae2 = [
    key
    for key, value in PROJECTS.items()
    if value.serial == SERIAL.AME and "2" in value.model
]


def get_component_name_by_project_name(project_name):
    if project_name in const_uro:
        return COMPONENT_FIX_VERSION.URO_Q
    if project_name in const_vhq:
        return COMPONENT_FIX_VERSION.VH2_OTA
    if project_name in const_vhs:
        return COMPONENT_FIX_VERSION.VAL_URO_S
    if project_name in const_ae1:
        return COMPONENT_FIX_VERSION.AE1_OTA
    if project_name in const_ae2:
        return COMPONENT_FIX_VERSION.AE2_OTA
    global_logger.warning(f"component related to project name {project_name} not found")
    return None


def get_component_name_by_module_id(module_id):
    if 0 == module_id:
        return COMPONENT_MODEL.VOICE_ASSISTANT
    elif 1 == module_id:
        return COMPONENT_MODEL.CONTROL_PROXY
    elif 2 == module_id:
        return COMPONENT_MODEL.KIDS_ELDER
    elif 3 == module_id:
        return COMPONENT_MODEL.ACCOUNT_APP
    elif 4 == module_id:
        return COMPONENT_MODEL.IOT
    elif 5 == module_id:
        return COMPONENT_MODEL.APP_ASSISTANT
    elif 6 == module_id:
        return COMPONENT_MODEL.BRAVIA_SHOW
    elif 7 == module_id:
        return COMPONENT_MODEL.PARTNER_KEY
    elif 8 == module_id:
        return COMPONENT_MODEL.MYSONY
    elif 9 == module_id:
        return COMPONENT_MODEL.CHINA_HOME
    else:
        global_logger.warning(f"component related to module id {module_id} not found")
