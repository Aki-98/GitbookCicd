import mjira.field
from mlogger import global_logger

from mgerrit.config import Project
from mjira.issue import Key
from typing import List

import re
import mio

import mgerrit.config

MESSAGE_TEMPLATE = """Update module to version_name

fixed_bugs

boc_config

Test: DQA
Test: Boot: PASS
Test: adb: PASS
Test: Display: PASS
Test: Sus/Res: PASS
Test: Youtube: N/A
Test: HDMI Video: PASS
Test: Broadcast: N/A
Test: USB Video: N/A
Test: USB Photo: N/A"""


PATTERN_BRANCH = r"branch:\s*(\S+)"
PATTERN_TAG = r"tag:\s*(\S+)"


def __get_boc_config(project: Project):
    boc_config_str = "\nBoC: OTA"
    if (
        project.serial == mgerrit.config.SERIAL.VAL
        or project.serial == mgerrit.config.SERIAL.URO
    ):
        boc_config_str = "BoC: cpkg\nBoC: Region= CNA,NCA\nBoC: OTA"
    elif project.serial == mgerrit.config.SERIAL.AME:
        boc_config_str = "BoC: Region= amaebi_cn\nBoC: OTA"
    return boc_config_str


def format_default_gerrit_message(
    module_name: str, version_name: str, project: Project
):
    boc_config_str = __get_boc_config(project)
    message = MESSAGE_TEMPLATE.replace("module", module_name)
    message = message.replace("version_name", version_name)
    message = message.replace("fixed_bugs", "")
    message = message.replace("boc_config", boc_config_str)
    return message


def format_custom_gerrit_message(
    module_name, version_name, project: Project, fixed_bug_key_list: List[Key]
):
    jira_id_str = ""
    if project.is_ota:
        for fixed_bug_key in fixed_bug_key_list:
            if fixed_bug_key.key_external:
                jira_id_str += "JIRA: " + fixed_bug_key.key_external + "\n"
    else:
        for fixed_bug_key in fixed_bug_key_list:
            if fixed_bug_key.key_external:
                jira_id_str += "JIRA: " + fixed_bug_key.key_external + "\n"
            if fixed_bug_key.key_internal:
                jira_id_str += "JIRA: " + fixed_bug_key.key_internal + "\n"

    boc_config_str = __get_boc_config(project)

    message = MESSAGE_TEMPLATE.replace("module", module_name)
    message = message.replace("version_name", version_name)
    message = message.replace("fixed_bugs", jira_id_str)
    message = message.replace("boc_config", boc_config_str)
    return message


def __edit_release_info(release_info_data_before, source_branch):
    branch_match = re.search(PATTERN_BRANCH, release_info_data_before)[0]
    tag_match = re.search(PATTERN_TAG, release_info_data_before)[0]
    global_logger.debug(f"Release Info Branch: {branch_match}")
    global_logger.debug(f"Release Info Tag: {tag_match}")

    if branch_match == source_branch and tag_match == "HEAD":
        return False

    release_info_data_after = release_info_data_before.replace(
        branch_match, f"branch: {source_branch}"
    )
    release_info_data_after = release_info_data_after.replace(tag_match, "tag: HEAD")
    global_logger.debug(release_info_data_after)
    return release_info_data_after


def confirm_and_update_release_info(path_submit_repo, release_info_name, source_branch):
    global_logger.debug("Confirm and Update release info...")
    pathall_release_info = mio.find_files(
        file_path=path_submit_repo, file_name=release_info_name
    )[0]
    data_release_info = mio.read_data_from_file(file_all_path=pathall_release_info)
    data_after_release_info = __edit_release_info(data_release_info, source_branch)
    if data_after_release_info:
        global_logger.debug("Replacing release info...")
        mio.write_data_to_file(
            file_all_path=pathall_release_info, data=data_after_release_info
        )


def __edit_notice_json(path_submit_repo, notice_json_name, app_gradle_path_all):
    # component_name
    # component_version
    return True


def __extract_dependencies_from_notice(notice_list: list) -> list:
    # Store extracted dependencies
    dependencies = []
    for notice_item in notice_list:
        dependencies.append(
            {
                "library": notice_item["component_name"],
                "version": notice_item["component_version"],
            }
        )
    return dependencies


def confirm_and_update_notice_json(
    path_submit_repo, notice_json_name, app_gradle_path_all
):
    global_logger.debug("Confirm and Update Notice Json...")
    pathall_notice_json = mio.find_files(
        file_path=path_submit_repo, file_name=notice_json_name
    )[0]
    notice_list = mio.get_json_from_file(file_all_path=pathall_notice_json)
    denpendencies_notice = __extract_dependencies_from_notice(notice_list)
    data_app_gradle = mio.read_data_from_file(file_all_path=app_gradle_path_all)
    denpendencies_gradle = extract_dependencies_from_gradle(data_app_gradle)
    # for dp_item_notice in denpendencies_notice:
    #     lib_name = dp_item_notice["library"]
    # for dp_item_gradle in denpendencies_gradle:
    # if lib_name in dp_item_gradle["library"]:
    # data_after_release_info = __edit_release_info(data_release_info, source_branch)
    # if data_after_release_info:
    #     global_logger.debug("Replacing release info...")
    #     mio.write_data_to_file(
    #         file_all_path=pathall_notice_json, data=data_after_release_info
    #     )
    return True
