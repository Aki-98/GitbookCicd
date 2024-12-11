from mjira.const import API, ISSUE_TYPE, ISSUELINK

from mlogger import global_logger
import mstr

import re, json
import mjira.field, mjira.issue, mjira.net


class Key:
    def __init__(
        self,
        summary: str = None,
        key_csc: str = None,
        key_external: str = None,
        key_internal: str = None,
        key_child: str = None,
        key_cnux_task: str = None,
        key_dqa_task: str = None,
        key_chandao: str = None,
        key_tapd: str = None,
    ):
        self.summary = summary
        self.key_csc = key_csc
        self.key_external = key_external
        self.key_internal = key_internal
        self.key_child = key_child
        self.key_cnux_task = key_cnux_task
        self.key_dqa_task = key_dqa_task
        self.key_chandao = key_chandao
        self.key_tapd = key_tapd

    def __str__(self):
        parts = []
        if self.summary:
            parts.append(f"summary={self.summary}")
        if self.key_csc:
            parts.append(f"key_csc={self.key_csc}")
        if self.key_external:
            parts.append(f"key_external={self.key_external}")
        if self.key_internal:
            parts.append(f"key_internal={self.key_internal}")
        if self.key_child:
            parts.append(f"key_child={self.key_child}")
        if self.key_cnux_task:
            parts.append(f"key_cnux_task={self.key_cnux_task}")
        if self.key_dqa_task:
            parts.append(f"key_dqa_task={self.key_dqa_task}")
        if self.key_chandao:
            parts.append(f"key_chandao={self.key_chandao}")
        if self.key_tapd:
            parts.append(f"key_tapd={self.key_tapd}")

        attr_str = ", ".join(parts)
        return f"Key({attr_str})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())

    def __bool__(self):
        for key, value in self.__dict__.items():
            if value not in (None, "", {}, []):
                return True
        return False

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            summary=data.get("summary"),
            key_csc=data.get("key_csc"),
            key_external=data.get("key_external"),
            key_internal=data.get("key_internal"),
            key_child=data.get("key_child"),
            key_cnux_task=data.get("key_cnux_task"),
            key_dqa_task=data.get("key_dqa_task"),
            key_chandao=data.get("key_chandao"),
            key_tapd=data.get("key_tapd"),
        )

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)


class Item(Key):
    def __init__(
        self,
        summary: str = None,
        key_csc: str = None,
        issue_csc: dict = None,
        key_external: str = None,
        issue_external: dict = None,
        key_child: str = None,
        issue_child: dict = None,
        key_internal: str = None,
        issue_internal: dict = None,
        key_dqa_task: str = None,
        key_chandao: str = None,
        key_tapd: str = None,
    ):
        super().__init__(
            summary=summary,
            key_csc=key_csc,
            key_external=key_external,
            key_internal=key_internal,
            key_child=key_child,
            key_dqa_task=key_dqa_task,
            key_chandao=key_chandao,
            key_tapd=key_tapd,
        )
        self.issue_csc = issue_csc
        self.issue_external = issue_external
        self.issue_child = issue_child
        self.issue_internal = issue_internal

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "issue_csc": self.issue_csc,
                "issue_external": self.issue_external,
                "issue_child": self.issue_child,
                "issue_internal": self.issue_internal,
            }
        )
        return data


# ------------------------ ID PATTERN ---------------------------

PATTERN_CNID = r"CHINAUX-\d+"
PATTERN_AMID = r"DM22TVSW-\d+"
PATTERN_VALID = r"DM20GN6-\d+"
PATTERN_BFID = r"DM24BLF-\d+"
PATTERN_DQA_TASK = r"CNUXDQID-\d+"
PATTERN_DQA_BUG = r"CNUXBTRACK-\d+"
PATTERN_CNUX_TASK = r"CNUXTASKS-\d+"
PATTERN_CHANDAO = r"\d{4}"
PATTERN_TAPD = r"\d{11,}"

CHANDAO_KEYWORDS = ["禅道", "dangbei"]
TAPD_KEYWORDS = ["tapd"]


def __extract_key_list(pattern: str, str: str):
    matches = re.findall(pattern, str)
    if matches and len(matches) == 1:
        return matches
    return []


def __extract_key(pattern: str, str: str):
    matches = __extract_key_list(pattern, str)
    return matches[0] if matches else ""


def extract_csc_key(str: str):
    return __extract_key(PATTERN_CNID, str)


def extract_csc_key_list(str: str):
    return __extract_key_list(PATTERN_CNID, str)


def extract_sony_key_list(str: str):
    matches = __extract_key_list(PATTERN_AMID, str)
    matches += __extract_key_list(PATTERN_VALID, str)
    matches += __extract_key_list(PATTERN_BFID, str)
    matches += __extract_key_list(PATTERN_DQA_BUG, str)
    return matches


def extract_internal_key_list(str: str):
    matches = __extract_key_list(PATTERN_DQA_BUG, str)
    return matches


def extract_external_key_list(str: str):
    matches = __extract_key_list(PATTERN_AMID, str)
    matches += __extract_key_list(PATTERN_VALID, str)
    matches += __extract_key_list(PATTERN_BFID, str)
    return matches


def extract_amaebi_key(str: str):
    return __extract_key(PATTERN_AMID, str)


def extract_valhalla_key(str: str):
    return __extract_key(PATTERN_VALID, str)


def extract_bluefin_key(str: str):
    return __extract_key(PATTERN_BFID, str)


def extract_dqa_task_key(str: str):
    return __extract_key(PATTERN_DQA_TASK, str)


def extract_internal_bug_key(str: str):
    return __extract_key(PATTERN_DQA_BUG, str)


def extract_cnux_task_key(str: str):
    return __extract_key(PATTERN_CNUX_TASK, str)


def extract_external_key(str: str):
    key_external = mjira.issue.extract_amaebi_key(str)
    if not key_external:
        key_external = mjira.issue.extract_valhalla_key(str)
    if not key_external:
        key_external = mjira.issue.extract_cnux_task_key(str)
    if not key_external:
        key_external = mjira.issue.extract_bluefin_key(str)
    return key_external


def extract_chandao_key(str: str) -> str:
    """Extracts a ZenTao (Chandao) ID.

    The string is considered a ZenTao ID only if it contains the keywords '禅道' or 'dangbei'.
    The return value is a 4-character string.
    """
    if mstr.check_str_in_array(str, CHANDAO_KEYWORDS):
        return __extract_key(PATTERN_CHANDAO, str)


def extract_tapd_key(str: str):
    if mstr.check_str_in_array(str, TAPD_KEYWORDS):
        return __extract_key(PATTERN_TAPD, str)


# ------------------------ ID FORMAT ---------------------------

FORMAT_TOKYO = API.HOST_TOKYO + API.END_BROWSE
FORMAT_CSC = API.HOST_CSC + API.END_BROWSE
FORMAT_TAPD = "https://tapd.tencent.com/tapd_fe/20452957/bug/detail/{id}"
FORMAT_CHANDAO_LINK = "https://otypm.dangbei.net/index.php?m=bug&f=view&t=html&id={id}"
FORMAT_CHANDAO = "禅道-{id}"


def format_csc_jira(str: str):
    csc_id = extract_csc_key(str)
    if csc_id:
        return FORMAT_CSC.format(csc_id)


def format_sony_jira(str: str):
    return FORMAT_TOKYO.format(str.strip())


def format_tapd_bug(str: str):
    tapd_id = extract_tapd_key(str)
    if tapd_id:
        return FORMAT_TAPD.format(id=tapd_id)


def format_chandao_link(str: str):
    chandao_id = extract_chandao_key(str)
    if chandao_id:
        return FORMAT_CHANDAO_LINK.format(id=chandao_id)


def format_chandao_bug(str: str):
    chandao_id = extract_chandao_key(str)
    if chandao_id:
        return FORMAT_CHANDAO.format(id=chandao_id)


# ------------------------ TYPE ---------------------------


def is_internal_bug_key(str: str):
    return True if extract_internal_bug_key(str) else False


def is_external_bug_key(str: str):
    return (
        True
        if (
            extract_amaebi_key(str)
            or extract_valhalla_key(str)
            or extract_bluefin_key(str)
        )
        else False
    )


def is_cnux_task_key(str: str):
    return True if extract_cnux_task_key(str) else False


# -------------- issue to key ------------------------


def get_external_bug_key_from_csc_issue(csc_issue: dict):
    """Should Never be used in mapping."""
    external_jira_field = mjira.field.get_external_jira_field(csc_issue)
    return extract_external_key(external_jira_field)


def get_child_bug_key_from_csc_issue(csc_issue: dict):
    """Should Never be used in mapping."""
    child_jira_field = mjira.field.get_child_jira_field(csc_issue)
    return extract_external_key(child_jira_field)


def get_internal_bug_key_from_csc_issue(csc_issue: dict):
    """Should Never be used in mapping."""
    internal_jira_field = mjira.field.get_internal_jira_field(csc_issue)
    return mjira.issue.extract_internal_bug_key(internal_jira_field)


def get_cnux_task_key_from_csc_issue(csc_issue: dict):
    """Should Never be used in mapping."""
    external_jira_field = mjira.field.get_external_jira_field(csc_issue)
    return mjira.issue.extract_cnux_task_key(external_jira_field)


def get_internal_bug_key_from_external_issue(issue_external: dict) -> str:
    """External Jira -- if issuelink is inwardIssue and bug key in Internal,
    linkname is Synchronizes/Relates/1.Relates, can never be Closers/Duplicate
    if mulpicate issue left calculate matched chars --> Internal Jira
    """
    issuelink_list = mjira.field.get_issue_link_list(issue_external)
    if not issuelink_list or len(issuelink_list) == 0:
        return ""
    inward_issuelink_list = mjira.field.get_inward_issuelink_list_from_issuelink_list(
        issuelink_list
    )
    if not inward_issuelink_list or len(inward_issuelink_list) == 0:
        return ""
    key = mjira.field.get_key(issue_external)
    matched_name_issuelink_list = []
    # Find Sync firstly
    for inward_issuelink in inward_issuelink_list:
        link_name = mjira.field.get_type_name_of_issuelink(inward_issuelink)
        if link_name in [ISSUELINK.SYNC]:
            matched_name_issuelink_list.append(inward_issuelink)
    # Find Relates secondly
    if len(matched_name_issuelink_list) == 0:
        for inward_issuelink in inward_issuelink_list:
            link_name = mjira.field.get_type_name_of_issuelink(inward_issuelink)
            if link_name in [ISSUELINK.RELATES, ISSUELINK.RELATES1]:
                matched_name_issuelink_list.append(inward_issuelink)
    # Find Other than Clone/Duplicate thirdly
    if len(matched_name_issuelink_list) == 0:
        for inward_issuelink in inward_issuelink_list:
            link_name = mjira.field.get_type_name_of_issuelink(inward_issuelink)
            if link_name not in [ISSUELINK.CLONE, ISSUELINK.DUPLICATE, ISSUELINK.BLOCK]:
                global_logger.warning(
                    f"link name: {link_name} detected in key: {mjira.field.get_key(inward_issuelink)}"
                )
                matched_name_issuelink_list.append(inward_issuelink)
    if len(matched_name_issuelink_list) == 0:
        return ""
    elif len(matched_name_issuelink_list) == 1:
        key, summary = mjira.field.get_key_summary_of_issuelink(
            matched_name_issuelink_list[0]
        )
        return key
    else:
        global_logger.warning(f"inward issue num detected is larger than 1")
        target_summary = mjira.field.get_summary(issue_external)
        global_logger.debug(
            f"external key: {mjira.field.get_key(issue_external)} summary: {target_summary}"
        )
        best_matched_value = 0.0
        best_matched_key = ""
        for matched_issuelink in matched_name_issuelink_list:
            key, summary = mjira.field.get_key_summary_of_issuelink(matched_issuelink)
            internal_bug_key = mjira.issue.extract_internal_bug_key(key)
            if internal_bug_key:
                fuzzy_match_value = mstr.fuzzy_match(target_summary, summary)
                if fuzzy_match_value > best_matched_value:
                    best_matched_value = fuzzy_match_value
                    best_matched_key = key
                global_logger.debug(
                    f"internal key: {key} match: {fuzzy_match_value} summary: {summary}"
                )
        global_logger.debug(f"best match internal key: {best_matched_key}")
        return best_matched_key


def get_external_key_from_internal_issue(issue_internal: dict) -> str:
    """Internal Jira -- if issuelink is outwardIssue and bug key in External,
    name is Synchronizes/Relates/1.Relates, can never be Closers/Duplicate,
    if mulpicate issue left then calculate matched chars. --> External Jira
    """
    issuelink_list = mjira.field.get_issue_link_list(issue_internal)
    if not issuelink_list or len(issuelink_list) == 0:
        return ""
    unfiltered_outward_issuelink_list = (
        mjira.field.get_outward_issuelink_list_from_issuelink_list(issuelink_list)
    )
    if (
        not unfiltered_outward_issuelink_list
        or len(unfiltered_outward_issuelink_list) == 0
    ):
        return ""
    outward_issuelink_list = []
    # Filter if Key in External...
    for outward_issuelink in unfiltered_outward_issuelink_list:
        key, _ = mjira.field.get_key_summary_of_issuelink(outward_issuelink)
        if mjira.issue.extract_external_key(key):
            outward_issuelink_list.append(outward_issuelink)
    if not outward_issuelink_list or len(outward_issuelink_list) == 0:
        return ""

    key = mjira.field.get_key(issue_internal)
    matched_name_issuelink_list = []

    # Find Sync firstly
    for outward_issuelink in outward_issuelink_list:
        link_name = mjira.field.get_type_name_of_issuelink(outward_issuelink)
        if link_name in [ISSUELINK.SYNC]:
            matched_name_issuelink_list.append(outward_issuelink)
    # Find Relates secondly
    if len(matched_name_issuelink_list) == 0:
        for outward_issuelink in outward_issuelink_list:
            link_name = mjira.field.get_type_name_of_issuelink(outward_issuelink)
            if link_name in [ISSUELINK.RELATES, ISSUELINK.RELATES1]:
                matched_name_issuelink_list.append(outward_issuelink)
    # Find Other than Clone/Duplicate thirdly
    if len(matched_name_issuelink_list) == 0:
        for outward_issuelink in outward_issuelink_list:
            link_name = mjira.field.get_type_name_of_issuelink(outward_issuelink)
            if link_name not in [
                ISSUELINK.CLONE,
                ISSUELINK.DUPLICATE,
                ISSUELINK.BLOCK,
                ISSUELINK.SPLIT,
            ]:
                global_logger.warning(
                    f"link name: {link_name} detected in key: {mjira.field.get_key(outward_issuelink)}"
                )
                matched_name_issuelink_list.append(outward_issuelink)
    if len(matched_name_issuelink_list) == 0:
        return ""
    elif len(matched_name_issuelink_list) == 1:
        key, summary = mjira.field.get_key_summary_of_issuelink(
            matched_name_issuelink_list[0]
        )
        return key
    else:
        global_logger.warning(f"outward issue num detected is larger than 1")
        target_summary = mjira.field.get_summary(issue_internal)
        global_logger.debug(
            f"external key: {mjira.field.get_key(issue_internal)} summary: {target_summary}"
        )
        best_matched_value = 0.0
        best_matched_key = ""
        for matched_issuelink in matched_name_issuelink_list:
            key, summary = mjira.field.get_key_summary_of_issuelink(matched_issuelink)
            fuzzy_match_value = mstr.fuzzy_match(target_summary, summary)
            if fuzzy_match_value > best_matched_value:
                best_matched_value = fuzzy_match_value
                best_matched_key = key
            global_logger.debug(
                f"external key: {key} match: {fuzzy_match_value} summary: {summary}"
            )
        global_logger.debug(f"best match external key: {best_matched_key}")
        return best_matched_key


def get_child_key_from_external_issue(issue_external: dict) -> str:
    """External Jira -- if contains subtask and jira type is Child,
    if mulpicate issue left then calculate matched chars. --> Child Jira"""
    subtask_list = mjira.field.get_subtask_list(issue_external)
    child_dict = {}
    for subtask in subtask_list:
        if ISSUE_TYPE.CHILD == mjira.field.get_issue_type(subtask):
            child_dict[mjira.field.get_key(subtask)] = mjira.field.get_summary(subtask)
    if len(child_dict) == 0:
        return ""
    elif len(child_dict) == 1:
        return next(iter(child_dict))
    else:
        global_logger.warning(f"child num detected is larger than 1")
        target_summary = mjira.field.get_summary(issue_external)
        global_logger.debug(
            f"external key: {mjira.field.get_key(issue_external)} summary: {target_summary}"
        )
        best_matched_value = 0.0
        best_matched_key = ""
        for key, summary in child_dict.items():
            fuzzy_match_value = mstr.fuzzy_match(target_summary, summary)
            if fuzzy_match_value > best_matched_value:
                best_matched_value = fuzzy_match_value
                best_matched_key = key
            global_logger.debug(
                f"child key: {key} match: {fuzzy_match_value} summary: {summary}"
            )
        global_logger.debug(f"best match child key: {best_matched_key}")
        return best_matched_key


def get_external_key_from_child_issue(issue_child: dict) -> str:
    """Child Jira -- if parent(the only) exist --> External Jira"""
    parent = mjira.field.get_parent(issue_child)
    if parent:
        external_key = mjira.field.get_key_of_parent(parent)
        return external_key
    return ""


# -----------------------------------------------------------


def search_all_key_from_any_key(input_str: str) -> Key:

    # Get Type of Id
    csc_id = mjira.issue.extract_csc_key(input_str)
    amaebi_id = mjira.issue.extract_amaebi_key(input_str)
    valhalla_id = mjira.issue.extract_valhalla_key(input_str)
    bluefin_id = mjira.issue.extract_bluefin_key(input_str)
    external_bug_id = None
    child_id = None
    internal_bug_id = mjira.issue.extract_internal_bug_key(input_str)
    cnux_task_id = mjira.issue.extract_cnux_task_key(input_str)
    dqa_task_id = mjira.issue.extract_dqa_task_key(input_str)
    tapd_id = mjira.issue.extract_tapd_key(input_str)
    chandao_id = mjira.issue.extract_chandao_key(input_str)

    # Get Csc Issue
    if csc_id:
        issue_csc = mjira.net.get_csc_jira(csc_id)
    elif cnux_task_id:
        issue_csc = mjira.net.search_csc_jira_by_external_jira(cnux_task_id)
    elif amaebi_id or valhalla_id or bluefin_id:
        adapted_id = (
            amaebi_id if amaebi_id else (valhalla_id if valhalla_id else bluefin_id)
        )
        issue_csc = mjira.net.search_csc_jira_by_external_jira(adapted_id)
        if issue_csc:
            external_bug_id = adapted_id
        else:
            issue_csc = mjira.net.search_csc_jira_by_child_jira(adapted_id)
            if issue_csc:
                child_id = adapted_id
    elif internal_bug_id:
        issue_csc = mjira.net.search_csc_jira_by_internal_jira(internal_bug_id)
    elif tapd_id or chandao_id:
        issue_csc = mjira.net.search_csc_jira_by_trd_id(tapd_id)
    else:
        global_logger.warning("id that entered not in format")
        return None

    if not issue_csc:
        global_logger.warning("related CSC JIRA not found")
        return None

    mkey = Key(
        summary=mjira.field.get_summary(issue_csc),
        key_csc=csc_id if csc_id else mjira.field.get_key(issue_csc),
        key_external=external_bug_id,
        key_child=child_id,
        key_internal=internal_bug_id,
        key_cnux_task=cnux_task_id,
        key_dqa_task=dqa_task_id,
        key_chandao=chandao_id,
        key_tapd=tapd_id,
    )

    # Get Tokyo Key from Csc Issue
    if not external_bug_id:
        external_bug_id = get_external_bug_key_from_csc_issue(issue_csc)
        mkey.key_external = external_bug_id

    if not internal_bug_id:
        internal_bug_id = get_internal_bug_key_from_csc_issue(issue_csc)
        mkey.key_internal = internal_bug_id

    if not child_id:
        child_id = get_child_bug_key_from_csc_issue(issue_csc)
        mkey.key_child = child_id

    if not (chandao_id or tapd_id):
        trd_party_link = mjira.field.get_trd_party(issue_csc)
        if trd_party_link:
            tapd_id = extract_tapd_key(input_str)
            if tapd_id:
                mkey.key_tapd = tapd_id
            else:
                chandao_id = extract_chandao_key(input_str)
                mkey.key_chandao = chandao_id

    return mkey
