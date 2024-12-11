from mjira.const import FIELD, FIELD_SONY, FIELD_CSC, ISSUE_TYPE

from mlogger import global_logger


def __get_value_of_json(json, *args):
    try:
        for arg in args:
            json = json.get(arg)
        if json or 0 == json:
            return json
        else:
            return ""
    except Exception as e:
        global_logger.warning(f"{e} happend when getting value {args}")
        return ""


# ------------------------ RESULTS ---------------------------


def get_total(results):
    return __get_value_of_json(results, FIELD.TOTAL)


def is_results_empty(results):
    total = get_total(results)
    return 0 == total


def get_issue_list(results):
    return __get_value_of_json(results, FIELD.ISSUES)


# ------------------------ ISSUE ---------------------------


def get_key(issue):
    return __get_value_of_json(issue, FIELD.KEY)


def get_assignee_name(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.ASSIGNEE, FIELD.NAME)


def get_fix_versions(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.FIX_VERSIONS)


def get_fix_version_list(issue):
    fix_version_list = []
    fix_versions = get_fix_versions(issue)
    if fix_versions and len(fix_versions) != 0:
        for fix_version in fix_versions:
            if fix_version:
                fix_version_name = __get_value_of_json(fix_version, FIELD.NAME)
                if fix_version_name:
                    fix_version_list.append(fix_version_name)
    return fix_version_list


def get_label_list(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.LABELS)


def get_status(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.STATUS, FIELD.NAME)


def get_priority(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.PRIORITY, FIELD.NAME)


def get_impact_scope(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.IMPACT_SCOPE)


def get_issue_type(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.ISSUETYPE, FIELD.NAME)


def get_release_jira(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.RELEASE_JIRA_ID)


def get_release_note_link(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.RELEASE_NOTE_LINK)


def get_summary(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.SUMMARY)


def get_description(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.DESCRIPTION)


def get_external_jira_field(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.EXTERNAL_JIRA)


def get_trd_party(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.TRDID)


def get_created_time(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.CREATED)


def get_comment_total(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.COMMENT, FIELD.TOTAL)


def get_pull_request_field(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.PULL_REQUEST)


def get_impact_scope(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.IMPACT_SCOPE)


def get_task_jira_id(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.TASK_JIRA_ID)


def get_external_issue_id(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_SONY.DQA_EXTERNAL_ISSUE_ID)


def get_release_package_tokyo(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_SONY.RELEASED_PACKAGE_VERSION)


def get_resolution(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.RESOLUTION)


def get_resolution_date(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.RESOLUTION_DATE)


def get_components(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.COMPONENTS)


def get_component_list(issue):
    component_list = []
    components = get_components(issue)
    for component in components:
        component_list.append(__get_value_of_json(component, FIELD.NAME))
    return component_list


def update_component_list(issue, new_component_list):
    components_json = []
    for component in new_component_list:
        components_json.append({FIELD.NAME: component})
    issue[FIELD.FIELDS][FIELD.COMPONENTS] = components_json
    return issue


def get_enviroment(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.ENVIRONMENT)


def get_modification_point(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.MODIFICATION_POINTS)


def get_child_id_list(issue):
    subtask_list = issue.get(FIELD.FIELDS, FIELD.SUBTASKS)
    child_id_list = []
    for subtask in subtask_list:
        child_id_list.append(__get_value_of_json(subtask, FIELD.ID))
    return child_id_list


def get_submit_branch(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.SUBMIT_BRANCH)


def update_submit_branch(issue, new_branch_value):
    issue[FIELD.FIELDS][FIELD.SUBMIT_BRANCH] = new_branch_value
    return issue


def get_weekly_report(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.WEEKLY_REPORT)


def get_subtask_list(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.SUBTASKS)


def get_release_pkg_version(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.RELEASED_PACKAGE_VERSION)


def get_deteced_sw_project_list(issue):
    deteced_sw_project_list = []
    try:
        deteced_sw_projects = __get_value_of_json(
            issue, FIELD.FIELDS, FIELD_SONY.DETECTED_SW_PROJECT
        )
        if not deteced_sw_projects:
            key = get_key(issue)
            global_logger.warning(
                f"deteced_sw_projects is empty in external jira {key}"
            )
            return deteced_sw_project_list
        for deteced_sw_project in deteced_sw_projects:
            deteced_sw_project_list.append(
                __get_value_of_json(deteced_sw_project, FIELD.VALUE)
            )
    except Exception as e:
        global_logger.warning(
            f"custom field of deteced_sw_projects not exist in external jira {key}"
        )
    return deteced_sw_project_list


def get_internal_jira_field(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.INTERNAL_JIRA)


def get_child_jira_field(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.CHILD_JIRA)


def get_defect_rank_auto(issue):
    defect_rank = __get_value_of_json(issue, FIELD.FIELDS, FIELD_SONY.DEFECT_RANK_AUTO)
    if defect_rank:
        return __get_value_of_json(defect_rank, FIELD.VALUE)
    return ""


def get_detected_version(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_SONY.DETECTED_VERSION)


def get_duedate(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.DUEDATE)


def get_defect_rank_csc(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.DEFECT_RANK)


def get_developer(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.DEVELOPER, FIELD.NAME)


def get_bug_jira_id(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.BUG_JIRA_ID)


def get_resolved_version(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.RESOLVED_VERSION)


def get_action_plan(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_SONY.ACTION_PLAN)


def get_dqa_test_result_filename(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.DQA_TEST_RESULT_FILENAME)


# ----------------------------------------- CSC ONLY -------------------------------------------
def get_boc_verify_result(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.BOC_VERIFY_RESULT)


def get_boc_test_result_filename(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.BOC_TEST_RESULT_FILENAME)


def get_boc_verify_conclusion(issue):
    return __get_value_of_json(
        issue, FIELD.FIELDS, FIELD_CSC.BOC_VERIFY_CONCLUSION, FIELD.VALUE
    )


def get_code_labels(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.CODE_LABELS)


def get_parent_id(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD_CSC.PARENT_ID)


def get_changelog(issue):
    return __get_value_of_json(issue, FIELD.CHANGELOG)


def get_history_list(issue):
    return __get_value_of_json(issue, FIELD.CHANGELOG, FIELD.HISTORYS)


# ------------------------ CHANGELOG ---------------------------


def get_changed_item_list(history: dict):
    return __get_value_of_json(history, FIELD.ITEMS)


def get_history_created_time(history):
    return __get_value_of_json(history, FIELD.CREATED)


def get_changed_item_field(changed_item: dict):
    return __get_value_of_json(changed_item, FIELD.FIELD)


def get_changed_item_from_string(changed_item: dict):
    return __get_value_of_json(changed_item, FIELD.FROM_STRING)


def get_changed_item_to_string(changed_item: dict):
    return __get_value_of_json(changed_item, FIELD.TO_STRING)


# ------------------------ WORKLOG ---------------------------


def get_worklog_total(worklog):
    return __get_value_of_json(worklog, FIELD.TOTAL)


def get_worklog_list(worklog):
    return __get_value_of_json(worklog, FIELD.WORKLOGS)


def get_worklog_author(worklog):
    return __get_value_of_json(worklog, FIELD.AUTHOR, FIELD.NAME)


def get_worklog_started(worklog):
    return __get_value_of_json(worklog, FIELD.STARTED)


def get_worklog_timespent_seconds(worklog):
    return __get_value_of_json(worklog, FIELD.TIMESPENTSECONDS)


# ------------------------ ISSUELINK ---------------------------


def get_issue_link_list(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.ISSUE_LINKS)


def get_type_name_of_issuelink(issuelink: dict) -> str:
    return __get_value_of_json(issuelink, FIELD.TYPE, FIELD.NAME)


def get_outward_issuelink_list_from_issuelink_list(issuelink_list: list) -> list:
    assert issuelink_list != None
    outward_issuelink_list = []
    for issuelink in issuelink_list:
        outward_issue = __get_value_of_json(issuelink, FIELD.OUTWARD_ISSUE)
        if outward_issue:
            outward_issuelink_list.append(issuelink)
    return outward_issuelink_list


def get_inward_issuelink_list_from_issuelink_list(issuelink_list: list) -> list:
    assert issuelink_list != None
    inward_issuelink_list = []
    for issuelink in issuelink_list:
        inward_issue = __get_value_of_json(issuelink, FIELD.INWARD_ISSUE)
        if inward_issue:
            inward_issuelink_list.append(issuelink)
    return inward_issuelink_list


def get_key_summary_of_issuelink(issuelink: dict) -> str:
    assert issuelink
    issue_field = __get_value_of_json(issuelink, FIELD.OUTWARD_ISSUE)
    if not issue_field:
        issue_field = __get_value_of_json(issuelink, FIELD.INWARD_ISSUE)
    assert issue_field != None
    key = __get_value_of_json(issue_field, FIELD.KEY)
    summary = __get_value_of_json(issue_field, FIELD.FIELDS, FIELD.SUMMARY)
    assert key != None
    assert summary != None
    return key, summary


def get_linked_bug_list(issuelink_list: list) -> str:
    assert issuelink_list != None
    bug_key_list = []

    for issuelink in issuelink_list:
        issue_field = __get_value_of_json(issuelink, FIELD.OUTWARD_ISSUE)
        if not issue_field:
            issue_field = __get_value_of_json(issuelink, FIELD.INWARD_ISSUE)
        assert issue_field != None

        key = __get_value_of_json(issue_field, FIELD.KEY)
        assert key != None

        issuetype = get_issue_type(issue_field)
        assert issuetype

        if issuetype == ISSUE_TYPE.BUG:
            bug_key_list.append(key)

    return bug_key_list


def get_linked_mt_list(issuelink_list: list) -> str:
    assert issuelink_list != None
    bug_key_list = []

    for issuelink in issuelink_list:
        issue_field = __get_value_of_json(issuelink, FIELD.OUTWARD_ISSUE)
        if not issue_field:
            issue_field = __get_value_of_json(issuelink, FIELD.INWARD_ISSUE)
        assert issue_field

        key = __get_value_of_json(issue_field, FIELD.KEY)
        assert key

        issuetype = get_issue_type(issue_field)
        assert issuetype

        if issuetype == ISSUE_TYPE.MT:
            bug_key_list.append(key)

    return bug_key_list


# ------------------------ PARENT ---------------------------


def get_parent(issue):
    return __get_value_of_json(issue, FIELD.FIELDS, FIELD.PARENT)


def get_key_of_parent(parent):
    return __get_value_of_json(parent, FIELD.KEY)
