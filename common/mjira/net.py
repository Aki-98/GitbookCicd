from mtime import TIME_ZONE_SHANGHAI
from mstr import ENCODE
from mauth import JIRA_TOKEN_CSC, JIRA_TOKEN_TOKYO
from mjira.const import API, FILTER, PROJECT, PROJECT_ID
from jira import JIRA
from urllib.request import Request, HTTPError

from mlogger import global_logger

from urllib.parse import quote
from urllib.request import urlopen
from json import loads, dumps

from mtime import get_current_datetime

import mjira.field
import mtoken

SPLIT_LEN = 50


# ------------------------ HTTP Root Methods ---------------------------


def __get_csc_headers(jira_user: str):
    token = mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
    return {
        "Content-Type": "application/json",
        "User-Agent": "JIRA",
        "Authorization": f"Bearer {token}",
    }


def __get_tokyo_headers(jira_user: str):
    token = mtoken.get_tokyo_jira_token(jira_user) if jira_user else JIRA_TOKEN_TOKYO
    return {
        "Content-Type": "application/json",
        "User-Agent": "JIRA",
        "Authorization": f"Bearer {token}",
    }


def __get_jira(headers: dict, url: str):
    """Retrieve detailed information from Jira using a Jira ID.

    This function retrieves detailed information for a specific Jira issue based on its ID.

    :param access_token: The access token for authorization.
    :param url: The URL endpoint for retrieving the Jira issue details.
    :return: The response body containing issue details in JSON format, or None if an error occurs.
    """
    try:
        global_logger.debug(f"get jira of url:{url}")
        request = Request(url=url, method="GET", headers=headers)
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return response_body
    except HTTPError as e:
        global_logger.warning(f"HTTP Error {e.code}: {e.reason}")
        global_logger.error(e.read())


def __search_jira(headers: dict, url: str, params=None):
    """Search Jira By Filter.

    This function performs a search in Jira using the provided URL and optional parameters.

    :param access_token: The access token for authorization.
    :param url: The URL endpoint for the Jira search request.
    :param params: Optional dictionary of parameters to refine the search.
    :return: The response body containing search results in JSON format, or None if an error occurs.
    """
    try:
        global_logger.debug(f"search jira of url:{url}")
        request = Request(url=url, method="GET", headers=headers)
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return response_body
    except HTTPError as e:
        # Handle HTTPError
        global_logger.warning(f"HTTP Error {e.code}: {e.reason}")
        global_logger.error(e.read())


def __put_jira(headers: dict, url: str, data: dict):
    """Update Jira information.

    This function updates an existing Jira issue with the provided data.

    :param access_token: The access token for authorization.
    :param url: The URL endpoint for updating the Jira issue.
    :param data: A dictionary containing the fields to update in the Jira issue.
    :return: The response body confirming the update in JSON format, or None if an error occurs.
    """
    try:
        global_logger.debug(f"put jira of url:{url} data{data}")
        request = Request(
            url, method="PUT", headers=headers, data=dumps(data).encode("utf-8")
        )
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return response_body
    except HTTPError as e:
        global_logger.warning(f"HTTP Error {e.code}: {e.reason}")
        global_logger.error(e.read())


def __post_jira(headers: dict, url: str, data: dict):
    """Create a new Jira issue.

    :param access_token: The access token for authorization.
    :param url: The URL endpoint for creating the issue.
    :param data: A dictionary containing the issue fields to be created.
    :return: The response body containing the created issue's details, or None if an error occurs.
    """
    try:
        global_logger.debug(f"post jira of url:{url} data{data}")
        request = Request(
            url, method="POST", headers=headers, data=dumps(data).encode("utf-8")
        )
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return response_body
    except HTTPError as e:
        global_logger.warning(f"HTTP Error {e.code}: {e.reason}")
        error_msg = e.read().decode("utf-8")
        global_logger.warning(error_msg)
        return error_msg


def __delete_jira(headers: dict, url: str):
    """Delete a Jira resource.

    :param access_token: The access token for authorization.
    :param url: The URL endpoint for deleting the resource.
    :return: True if the resource was deleted successfully, False if an error occurs.
    """
    try:
        global_logger.debug(f"delete jira of url: {url}")
        request = Request(url, method="DELETE", headers=headers)
        response = urlopen(request)

        if response.status == 204:
            global_logger.info(f"Resource deleted successfully at {url}")
            return True
        else:
            global_logger.warning(f"Unexpected response status: {response.status}")
            return False
    except HTTPError as e:
        global_logger.warning(f"HTTP Error {e.code}: {e.reason}")
        global_logger.error(e.read())
        return False


# ------------------------ HTTP CSC Methods ---------------------------


def get_csc_jira(key: str, jira_user: str = None):
    """Fetch the details of a CSC Jira issue by its key.

    :param key: The key of the Jira issue to retrieve.
    :return: JSON object containing issue details.
    """
    json_results = loads(
        __get_jira(__get_csc_headers(jira_user), API.CSC_ISSUE.format(key))
    )
    return json_results


def get_csc_jira_changelog(key: str, jira_user: str = None):
    """Fetch the change log of a CSC Jira issue.

    ChangeLog is the record of changes in Jira, along with the basic returned data.

    :param key: The key of the Jira issue to retrieve the changelog for.
    :return: JSON object containing the issue changelog.
    """
    json_results = loads(
        __get_jira(__get_csc_headers(jira_user), API.CSC_ISSUE_CHANGELOG.format(key))
    )
    return json_results


def get_csc_jira_worklog(key: str, jira_user: str = None):
    """Fetch the work log of a CSC Jira issue.

    WorkLog is the log of work in Jira, without basic return data.

    :param key: The key of the Jira issue to retrieve the worklog for.
    :return: JSON object containing the issue worklog.
    """
    json_results = loads(
        __get_jira(__get_csc_headers(jira_user), API.CSC_ISSUE_WORKLOG.format(key))
    )
    return json_results


def get_csc_jira_fixversion_list(jira_user: str = None):
    """Retrieve the list of available fix versions for the CSC Jira Center ChinaUX Project.

    :return: List of names of available fix versions.
    """
    json_results = loads(
        __get_jira(__get_csc_headers(jira_user), API.CSC_GET_FIXVERSIONS)
    )
    name_list = [item["name"] for item in json_results]
    return name_list


def create_csc_jira_fixversion(fix_version: str, jira_user: str = None):
    assert fix_version
    headers = __get_csc_headers(jira_user)
    data = {
        "description": fix_version,
        "name": fix_version,
        "archived": False,
        "released": False,
        "project": PROJECT.CHINAUX,
        "projectId": PROJECT_ID.CHINAUX,
    }
    json_results = loads(__post_jira(headers, API.CSC_CREATE_FIXVERSION, data))
    return json_results


def search_csc_jira_split(filter: str, split_seq: int, jira_user: str = None):
    """Search for CSC Jira issues with pagination support.

    :param filter: The JQL filter string to search for issues.
    :param split_seq: The page number to retrieve, used for pagination.
    :return: JSON object containing the search results.
    """
    json_results = loads(
        __search_jira(
            __get_csc_headers(jira_user),
            API.CSC_SEARCH_SPLITED.format(
                jql=quote(filter), start_at=split_seq * SPLIT_LEN, max_results=SPLIT_LEN
            ),
        )
    )
    return json_results


def update_csc_jira(key: str, data: dict, jira_user: str = None):
    """Update a CSC Jira issue with new data.

    :param key: The key of the Jira issue to update.
    :param data: A dictionary containing the fields to update.
    :return: None
    """
    return __put_jira(__get_csc_headers(jira_user), API.CSC_UPDATE.format(key), data)


def link_csc_jira(
    issue_key_1, issue_key_2, link_type, comment=None, jira_user: str = None
):
    """Link two Jira issues in the CSC project.

    This function creates a link between two Jira issues of a specified link type.

    :param issue_key_1: The key of the first issue to link (inward issue).
    :param issue_key_2: The key of the second issue to link (outward issue).
    :param link_type: The type of link to create (e.g., "relates to", "blocks").
    :param comment: Optional comment to add to the link. Defaults to None.
    :return: The response from the Jira API indicating the success or failure of the linking operation.
    """
    payload = {
        "type": {"name": link_type},
        "inwardIssue": {"key": issue_key_1},
        "outwardIssue": {"key": issue_key_2},
    }
    if comment:
        payload["comment"] = {"body": comment}
    return __post_jira(__get_csc_headers(jira_user), API.CSC_LINK_ISSUE, payload)


def get_csc_issue_attachments(issue_key, jira_user: str = None):
    """
    Get the attachment list of a specific Issue
    :param issue_key: JIRA Issue key (e.g., "ISSUE-123")
    :return: A list of attachment information, each containing id and filename
    """
    url = API.CSC_GET_JIRA_ATTACHMENTS.format(issue_key)
    json_results = loads(__get_jira(__get_csc_headers(jira_user), url))
    return json_results


def delete_csc_attachment(attachment_id, jira_user: str = None):
    """
    Delete an attachment by its ID
    :param attachment_id: The ID of the attachment
    :return: None
    """
    url = API.CSC_DEL_JIRA_ATTACHMENT.format(attachment_id)
    execution = __delete_jira(__get_csc_headers(jira_user), url)
    return execution


# ------------------------ HTTP Tokyo Methods ---------------------------


def search_tokyo_jira(filter: str, jira_user: str = None):
    """Search for Tokyo Jira issues.

    :param filter: The JQL filter string to search for issues.
    :return: JSON object containing the search results.
    """
    json_results = loads(
        __search_jira(
            __get_tokyo_headers(jira_user), API.TOKYO_SEARCH.format(quote(filter))
        )
    )
    return json_results


def search_tokyo_jira_in_params(
    filter: str, field_list: list, max_results: int = -1, jira_user: str = None
):
    """Search for Tokyo Jira issues with specific fields.

    :param filter: The JQL filter string to search for issues.
    :param field_list: A list of fields to include in the results.
    :param max_results: Maximum number of results to return; -1 for no limit.
    :return: JSON object containing the search results.
    """
    fields = ",".join(field_list)
    url = API.TOKYO_SEARCH_PARMAS.format(
        jql=quote(filter), fields=fields, max_results=max_results
    )
    json_results = loads(__search_jira(__get_tokyo_headers(jira_user), url))
    return json_results


def search_tokyo_jira_expand_changelog_split(
    filter: str, split_seq: int, jira_user: str = None
):
    """Search for Tokyo Jira issues with changelog and pagination support.

    :param filter: The JQL filter string to search for issues.
    :param split_seq: The page number to retrieve, used for pagination.
    :return: JSON object containing the search results with changelog.
    """
    json_results = loads(
        __search_jira(
            __get_tokyo_headers(jira_user),
            API.TOKYO_SEARCH_CHANGELOG_SPLITED.format(
                jql=quote(filter), start_at=split_seq * SPLIT_LEN, max_results=SPLIT_LEN
            ),
        )
    )
    return json_results


def get_sony_jira(key: str, jira_user: str = None):
    """Fetch the details of a Tokyo Jira issue by its key.

    :param key: The key of the Jira issue to retrieve.
    :return: JSON object containing issue details.
    """
    json_results = loads(
        __get_jira(__get_tokyo_headers(jira_user), API.TOKYO_ISSUE.format(key))
    )
    return json_results


# ------------------------ CSC Jira Methods ---------------------------


def search_csc_jira(filter: str, jira_user: str = None):
    """Search for CSC Jira issues using the expand method.

    :param filter: The JQL filter string to search for issues.
    :return: The search results.
    """
    global_logger.debug(f"search csc jira called with filter: {filter}")
    return search_csc_jira_expand(filter, expand=None, fields=None, json_result=True)


def search_csc_jira_expand(
    filter: str,
    expand: str = "changelog",
    fields=None,
    json_result: bool = False,
    jira_user: str = None,
):
    """Search for CSC Jira issues with the option to expand fields.

    :param filter: The JQL filter string to search for issues.
    :param expand: Optional fields to expand in the results.
    :param fields: Specific fields to include in the results.
    :param json_result: Whether to return the results as JSON.
    :return: The search results.
    """
    global_logger.debug(
        f"search csc jira expand called with filter: {filter}, expand: {expand}, fields: {fields}"
    )
    jira_conn = JIRA(
        server=API.HOST_CSC,
        token_auth=(
            mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
        ),
    )
    results = jira_conn.search_issues(
        filter, expand=expand, fields=fields, maxResults=-1, json_result=json_result
    )
    return results


def __search_csc_jira_by_filter_id(filter_id, jira_user: str = None):
    """Search for a CSC Jira issue by filter ID.

    Only returns a unique ID result. If not unique, it must be modified in the CSC system.

    :param filter_id: The filter ID to search for.
    :return: The unique issue if found, otherwise None.
    """
    global_logger.debug(f"search csc jira by filter ID: {filter_id}")
    result_internal = search_csc_jira(filter_id, jira_user)
    total = mjira.field.get_total(result_internal)
    if not total or 0 == total:
        global_logger.warning(f"CSC Jira of {filter_id} is not found.")
    elif 1 == total:
        issues = mjira.field.get_issue_list(result_internal)
        return issues[0]
    else:
        issues = mjira.field.get_issue_list(result_internal)
        for issue in issues:
            global_logger.warning(f"{mjira.field.get_key(issue)}")
        global_logger.warning(f"there are {total} CSC Jira for {filter_id}.")


def search_csc_jira_by_internal_jira(dqa_bug, jira_user: str = None):
    """Get the corresponding CSC Jira by Internal Jira ID.

    :param dqa_bug: The internal Jira ID to search for.
    :return: The corresponding CSC Jira issue if found, otherwise None.
    """
    global_logger.debug(f"search csc jira by internal jira ID: {dqa_bug}")
    filter_id = FILTER.INTERNAL_KEY.format(dqa_bug)
    return __search_csc_jira_by_filter_id(filter_id, jira_user)


def search_csc_jira_by_tokyo_id(tokyo_id, jira_user: str = None):
    """Get the corresponding CSC Jira by External Jira + Child Jira ID.

    :param tokyo_id: The Tokyo ID to search for.
    :return: The corresponding CSC Jira issue if found, otherwise None.
    """
    global_logger.debug(f"search csc jira by tokyo ID: {tokyo_id}")
    filter_id = FILTER.TOKYO_KEY.format(tokyo_id)
    return __search_csc_jira_by_filter_id(filter_id, jira_user)


def search_csc_jira_by_external_jira(tokyo_id, jira_user: str = None):
    """Get the corresponding CSC Jira by External Jira ID.

    :param tokyo_id: The Tokyo ID to search for.
    :return: The corresponding CSC Jira issue if found, otherwise None.
    """
    global_logger.debug(f"search csc jira by external jira ID: {tokyo_id}")
    filter_id = FILTER.EXTERNAL_KEY.format(tokyo_id)
    return __search_csc_jira_by_filter_id(filter_id, jira_user)


def search_csc_jira_by_child_jira(tokyo_id, jira_user: str = None):
    """Get the corresponding CSC Jira by Child Jira ID.

    :param tokyo_id: The Tokyo ID to search for.
    :return: The corresponding CSC Jira issue if found, otherwise None.
    """
    global_logger.debug(f"search csc jira by child jira ID: {tokyo_id}")
    filter_id = FILTER.CHILD_KEY.format(tokyo_id)
    return __search_csc_jira_by_filter_id(filter_id, jira_user)


def search_csc_jira_by_trd_id(tokyo_id, jira_user: str = None):
    """Get the corresponding CSC Jira by Third Party ID.

    :param tokyo_id: The Tokyo ID to search for.
    :return: The corresponding CSC Jira issue if found, otherwise None.
    """
    global_logger.debug(f"search csc jira by third party ID: {tokyo_id}")
    filter_id = FILTER.TRD_KEY.format(tokyo_id)
    return __search_csc_jira_by_filter_id(filter_id, jira_user)


def create_csc_jira(data_issue: dict, jira_user: str = None):
    """Create a new CSC Jira issue.

    :param data_issue: A dictionary containing the fields of the issue to be created.
    :return: The key of the newly created issue.
    """
    global_logger.debug(f"creating CSC jira with data: {data_issue}")
    try:
        jira_conn = JIRA(
            server=API.HOST_CSC,
            token_auth=(
                mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
            ),
        )
        issue = jira_conn.create_issue(fields=data_issue)
        global_logger.info("Issue created successfully!")
        return issue.key
    except Exception as e:
        global_logger.error(f"Failed to create issue in CSC Jira: {e}")
        raise


def transition_csc_jira(key: str, new_status: str, jira_user: str = None):
    """Transition a CSC Jira issue to a new status.

    :param key: The key of the Jira issue to transition.
    :param new_status: The new status to which the issue should be transitioned.
    :return: None
    """
    global_logger.debug(f"transitioning CSC jira {key} to status {new_status}")
    try:
        jira_conn = JIRA(
            server=API.HOST_CSC,
            token_auth=(
                mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
            ),
        )
        issue = jira_conn.issue(key)
        jira_conn.transition_issue(issue, transition=new_status)
        global_logger.info("Issue transitioned successfully!")
    except Exception as e:
        global_logger.error("Exception: " + str(e))


def transition_csc_jira_fields(
    key: str, new_status: str, fields: dict, jira_user: str = None
):
    """Transition a CSC Jira issue to a new status with additional fields.

    :param key: The key of the Jira issue to transition.
    :param new_status: The new status to which the issue should be transitioned.
    :param fields: A dictionary of additional fields to update during the transition.
    :return: None
    """
    global_logger.debug(
        f"transitioning CSC jira {key} to status {new_status} with fields {fields}"
    )
    try:
        jira_conn = JIRA(
            server=API.HOST_CSC,
            token_auth=(
                mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
            ),
        )
        issue = jira_conn.issue(key)
        jira_conn.transition_issue(issue, transition=new_status, fields=fields)
        global_logger.info("Issue transitioned successfully!")
    except Exception as e:
        global_logger.error("Exception: " + str(e))


def add_comment_csc_jira(key: str, comment: str, jira_user: str = None):
    """Add a comment to a CSC Jira issue.

    :param key: The key of the Jira issue to which the comment should be added.
    :param comment: The content of the comment to be added.
    :return: None
    """
    global_logger.debug(f"adding comment to CSC jira {key}: {comment}")
    try:
        jira_conn = JIRA(
            server=API.HOST_CSC,
            token_auth=(
                mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
            ),
        )
        issue = jira_conn.issue(key)
        jira_conn.add_comment(issue, comment)
        global_logger.info("Comment added successfully!")
    except Exception as e:
        global_logger.error("Exception: " + str(e))


def add_worklog_csc_jira(
    key: str, timeSpent: str, comment: str = "整理", jira_user: str = None
):
    """Add a worklog to a specific Jira issue.

    :param key: The key of the Jira issue to which the worklog should be added.
    :param timeSpent: The amount of time spent on the issue (e.g., '1h', '30m', '0.5d').
    :param comment: An optional comment for the worklog (default is "整理").
    :return: None
    """
    global_logger.debug(
        f"adding worklog to CSC jira {key} with timeSpent: {timeSpent} and comment: {comment}"
    )
    try:
        jira_conn = JIRA(
            server=API.HOST_CSC,
            token_auth=(
                mtoken.get_csc_jira_token(jira_user) if jira_user else JIRA_TOKEN_CSC
            ),
        )
        issue = jira_conn.issue(key)
        jira_conn.add_worklog(
            issue=issue,
            timeSpent=timeSpent,
            started=get_current_datetime(tz=TIME_ZONE_SHANGHAI),
            comment=comment,
        )
        global_logger.info("Worklog added successfully!")
    except Exception as e:
        global_logger.error("Exception: " + str(e))


# ------------------------ JIRA TOKYO Methods ---------------------------


def create_tokyo_jira(data_issue: dict, jira_user: str = None):
    """Create a new Tokyo Jira issue.

    :param data_issue: A dictionary containing the fields for the new issue.
    :return: The key of the created issue if successful; otherwise, None.
    """
    global_logger.debug(f"creating Tokyo jira with data: {data_issue}")
    try:
        jira_conn = JIRA(
            server=API.HOST_TOKYO,
            token_auth=(
                mtoken.get_tokyo_jira_token(jira_user)
                if jira_user
                else JIRA_TOKEN_TOKYO
            ),
        )
        response = jira_conn.create_issue(fields=data_issue)
        global_logger.info("Issue created successfully!")
        global_logger.info(f"Issue key: {response.key}")
        return response.key
    except Exception as e:
        global_logger.error("Exception: " + str(e))
        return None


def update_tokyo_jira(key: str, data_issue: dict, jira_user: str = None):
    """Update an existing Tokyo Jira issue.

    :param key: The key of the Jira issue to update.
    :param data_issue: A dictionary containing the fields to update.
    :return: None
    """
    global_logger.debug(f"updating Tokyo jira {key} with data: {data_issue}")
    try:
        jira_conn = JIRA(
            server=API.HOST_TOKYO,
            token_auth=(
                mtoken.get_tokyo_jira_token(jira_user)
                if jira_user
                else JIRA_TOKEN_TOKYO
            ),
        )
        issue = jira_conn.issue(key)
        issue.update(fields=data_issue)
        global_logger.info("Issue updated successfully!")
    except Exception as e:
        global_logger.error("Exception: " + str(e))


def transition_tokyo_jira_fields(
    key: str, new_status: str, fields: dict, jira_user: str = None
):
    """Transition a Tokyo Jira issue to a new status with additional fields.

    :param key: The key of the Jira issue to transition.
    :param new_status: The new status to which the issue should be transitioned.
    :param fields: A dictionary of additional fields to update during the transition.
    :return: None
    """
    global_logger.debug(
        f"transitioning Tokyo jira {key} to status {new_status} with fields: {fields}"
    )
    try:
        jira_conn = JIRA(
            server=API.HOST_TOKYO,
            token_auth=(
                mtoken.get_tokyo_jira_token(jira_user)
                if jira_user
                else JIRA_TOKEN_TOKYO
            ),
        )
        issue = jira_conn.issue(key)
        jira_conn.transition_issue(issue, transition=new_status, fields=fields)
        global_logger.info("Issue transited successfully!")
    except Exception as e:
        global_logger.error("Exception: " + str(e))
