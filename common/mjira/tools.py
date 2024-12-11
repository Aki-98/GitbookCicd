from mjira.field import FIELD
from mmodule.provider import MODULE_LIST

from mlogger import global_logger

import mstr
import mgithub

import mjira.field
import mjira.issue
import mjira.net

import mmodule.provider


def check_csc_jira_issue_type(jira_issue: dict, issue_type: str):
    jira_type = mjira.field.get_issue_type(jira_issue)
    if not jira_type:
        global_logger.error(f"{jira_type} is empty!!!")
    if jira_type == issue_type:
        return jira_issue
    else:
        return None


def check_csc_jira_id_type(jira_id: str, issue_type: str):
    jira_id = mjira.issue.extract_csc_key(jira_id)
    if not jira_id:
        global_logger.error(f"{jira_id} is not a csc jira key")
    jira_issue = mjira.net.get_csc_jira(jira_id)
    return check_csc_jira_issue_type(jira_issue, issue_type)


def fix_version_has_monitoring(jira_issue: dict) -> bool:
    fix_version_list = mjira.field.get_fix_version_list(jira_issue)
    if fix_version_list:
        for fix_version in fix_version_list:
            if "monitoring" in fix_version.lower():
                global_logger.debug(
                    f"fix version of {mjira.field.get_key(jira_issue)} has monitoring, skipping...",
                )
                return True
    return False


def fix_version_has_temporary(jira_issue: dict) -> bool:
    fix_version_list = mjira.field.get_fix_version_list(jira_issue)
    if fix_version_list:
        for fix_version in fix_version_list:
            if "temporary" in fix_version.lower():
                global_logger.debug(
                    f"fix version of {mjira.field.get_key(jira_issue)} has temporary, skipping...",
                )
                return True
    return False


def get_module_component_of_csc_issue(jira_issue: dict) -> set:
    component_list_original = mjira.field.get_component_list(jira_issue)
    model_component_list_all = mmodule.provider.get_module_component_list()
    model_component_list_detected = []
    for component in model_component_list_all:
        if component in component_list_original:
            model_component_list_detected.append(component)
            break
    return model_component_list_detected


def alter_mt_from_pull_request(mt_issue: dict):
    mt_key = mjira.field.get_key(mt_issue)
    pull_request_field = mjira.field.get_pull_request_field(mt_issue)
    pull_request_link_list = mstr.extract_pr_list(pull_request_field)

    if not pull_request_link_list or len(pull_request_link_list) == 0:
        global_logger.warning(
            f"no github pull request in modification task > {mt_key} pull_request_field > {pull_request_field}"
        )
        return None

    submit_branch_target = ""
    module_component = ""
    project_component = ""

    for pull_request_link in pull_request_link_list:
        pr_org, pr_repo, pr_num = mstr.extract_pr_info(pull_request_link)
        if not pr_repo or not pr_num:
            global_logger.debug(
                f"info extractted from pr is incorret, org:{pr_org} repo:{pr_repo} num:{pr_num}"
            )
        # 1. submit_branch
        base_branch = mgithub.get_pr_base(pr_repo, pr_num)
        if base_branch not in submit_branch_target:
            submit_branch_target += base_branch + "; "
        else:
            global_logger.warning(
                f"base_branch {base_branch} is duplicate in {submit_branch_target}"
            )
        # 2. model_components
        for module in MODULE_LIST:
            if pr_repo == module.module_path.source_repo:
                module_component = module.component
                break
        if module_component:
            break
        # # 3. project_components
        # for module in MODULE_LIST:
        #     for branch, project in module.source_branch.items():
        #         if branch == base_branch:
        #             project_component = project[0].component
        #             break
        #     if project_component:
        #         break

    submit_branch_origin = ""
    submit_branch_origin = mjira.field.get_submit_branch(mt_issue)

    component_list_original = mjira.field.get_component_list(mt_issue)

    data_to_update = {}

    if (
        submit_branch_origin.replace(";", "").replace("；", "").strip()
        != submit_branch_target.replace(";", "").replace("；", "").strip()
    ):
        global_logger.info(
            f"submit branch needs to be updated to > {submit_branch_target} origin > {submit_branch_origin}"
        )
        data_to_update[FIELD.SUBMIT_BRANCH] = submit_branch_target
        mt_issue = mjira.field.update_submit_branch(mt_issue, submit_branch_target)

    if module_component:
        component_list_target = set(component_list_original + [module_component])
        component_list_original = set(component_list_original)
        if component_list_original != component_list_target:
            global_logger.info(
                f"component list needs to be updated to > {component_list_target} origin > {component_list_original}"
            )
            data_to_update[FIELD.COMPONENTS] = []
            for module_component in component_list_target:
                data_to_update[FIELD.COMPONENTS].append({FIELD.NAME: module_component})
            mt_issue = mjira.field.update_component_list(
                mt_issue, component_list_target
            )

    if data_to_update:
        global_logger.debug(f"data to update > {data_to_update}")
        mjira.net.update_csc_jira(mt_key, {FIELD.FIELDS: data_to_update})

    return mt_issue
