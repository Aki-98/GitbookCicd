class API:

    # Format: Host + Api + End
    HOST_TOKYO = "https://www.tool.sony.biz/tv-jira"
    HOST_CSC = "https://csc-jira.sony.com.cn"

    API_JIRA = "/rest/api/2/"

    END_SERVER_INFO = "serverInfo"
    END_PROJECT = "project"
    END_ISSUE = "issue/{}"
    END_ISSUE_CHANGELOG = "issue/{}?expand=changelog"
    END_ISSUE_WORKLOG = "issue/{}/worklog"
    END_ISSUE_ATTACHMENT = "issue/{}?fields=attachment"
    END_SEARCH = "search?jql={}&maxResults=-1"
    END_SEARCH_PARAMS = "search?jql={jql}&fields={fields}&maxResults={max_results}"
    END_SEARCH_CHANGELOG_SPLITED = (
        "search?jql={jql}&expand=changelog&startAt={start_at}&maxResults={max_results}"
    )
    END_SEARCH_SPLITED = "search?jql={jql}&startAt={start_at}&maxResults={max_results}"
    END_BROWSE = "/browse/{}"
    END_CREATE = "issue"
    END_TRANSITIONS = "transitions"
    END_ISSUELINK = "issueLink"
    END_DEL_ATTACHMENT = "attachment/{}"

    TOKYO_ISSUE = HOST_TOKYO + API_JIRA + END_ISSUE
    TOKYO_SEARCH = HOST_TOKYO + API_JIRA + END_SEARCH
    TOKYO_SEARCH_PARMAS = HOST_TOKYO + API_JIRA + END_SEARCH_PARAMS
    TOKYO_SEARCH_CHANGELOG_SPLITED = (
        HOST_TOKYO + API_JIRA + END_SEARCH_CHANGELOG_SPLITED
    )
    TOKYO_CREATE = HOST_TOKYO + API_JIRA + END_CREATE

    CSC_ISSUE = HOST_CSC + API_JIRA + END_ISSUE
    CSC_ISSUE_CHANGELOG = HOST_CSC + API_JIRA + END_ISSUE_CHANGELOG
    CSC_ISSUE_WORKLOG = HOST_CSC + API_JIRA + END_ISSUE_WORKLOG
    CSC_SEARCH = HOST_CSC + API_JIRA + END_SEARCH
    CSC_SEARCH_SPLITED = HOST_CSC + API_JIRA + END_SEARCH_SPLITED
    CSC_CREATE = HOST_CSC + API_JIRA + END_CREATE
    CSC_TRANSITIONS = HOST_CSC + API_JIRA + END_TRANSITIONS
    CSC_UPDATE = HOST_CSC + API_JIRA + END_ISSUE
    CSC_CREATE_FIXVERSION = "https://csc-jira.sony.com.cn/rest/api/2/version"
    CSC_GET_FIXVERSIONS = (
        "https://csc-jira.sony.com.cn/rest/api/2/project/CHINAUX/versions"
    )
    CSC_LINK_ISSUE = HOST_CSC + API_JIRA + END_ISSUELINK

    CSC_GET_JIRA_ATTACHMENTS = HOST_CSC + API_JIRA + END_ISSUE_ATTACHMENT
    CSC_DEL_JIRA_ATTACHMENT = HOST_CSC + API_JIRA + END_DEL_ATTACHMENT


class FILTER:
    # Do not use this filtering condition: AND fixVersion not in ("Quality Moitoring", QualityMonitoring),
    # it will cause bugs without fixVersion to be unsearchable.
    # ChinaUX-H is HCL, not within our team.
    ALL_BUG = 'project in (DM22TVSW, DM20GN6, CNUXBTRACK, ChinaUX_Task_Tracking) AND issuetype in (Bug, "Change Spec", Task, Todo) AND status not in (Closed, Released, Verified, Resolved, Deferred) AND component = ChinaUX AND assignee not in (5106002624) AND key not in (DM20GN6-54909,CNUXBTRACK-97)'
    ALL_UPDATE = '(project in (DM22TVSW, DM20GN6, CNUXBTRACK) AND issuetype in (Bug, "Change Spec", Task, Todo) AND component = ChinaUX AND assignee not in (5106002624) AND updated >= "{time}") OR (project = ChinaUX_Task_Tracking AND assignee in (5109201548,5109U26356) AND created >= "{time}")'

    CHINAUX_TASK = 'project = ChinaUX_Task_Tracking AND assignee in (5109201548,5109U26356) AND created >= "{}"'
    CHINAUX_TASK_CREATE = 'project = ChinaUX_Task_Tracking AND assignee in (5109201548,5109U26356) AND created >= "{}"'

    LONG_NOT_DONE = 'project = CHINAUX AND status in (OPEN, "IN PROGRESS", Reopened, Assigned, Implementing, "Wait for Review", "Prepare for Submit", "DQA Verifying", "FL Judge DQA", "BoC Verifying", "FL Judge BoC") AND created <=  startOfDay(-140)'
    LONG_NO_RESPONSE = 'project = CHINAUX AND issuetype in (Bug) AND status in (OPEN, "IN PROGRESS", Reopened, Assigned, Implementing, "Wait for Review", "Prepare for Submit", "DQA Verifying", "FL Judge DQA", "BoC Verifying", "FL Judge BoC") AND created <=  startOfDay(-3) AND updated <= startOfDay(-3)'
    LONG_NOT_UPDATED = 'project = CHINAUX AND issuetype in (Bug) AND priority in (Major) AND status in (OPEN, "IN PROGRESS", Reopened, Assigned, Implementing, "Wait for Review", "Prepare for Submit", "DQA Verifying", "FL Judge DQA", "BoC Verifying", "FL Judge BoC") AND createdDate <= startOfDay(-7) AND updated <= startOfDay(-7)'

    BUGS_TRD_PARTY = 'project in (ChinaUX) AND issuetype in (Bug) AND "3rd-party bug ID" is not EMPTY'
    MT_BUGS = 'project in (ChinaUX) AND issuetype in ("Modification Task") AND "Impact Scope" is not EMPTY'
    BUGS_TAPD_OPEN = 'issuetype = Bug AND project in (ChinaUX) AND status not in (Resolved, Closed) AND "3rd-party bug ID" ~"tapd"'

    MT_NO_SUBMIT_BRANCH = 'project = ChinaUX AND issuetype = "Modification Task" AND "Submit Branch" is EMPTY AND "Pull Request Link"  is not EMPTY  AND status  not in (Abandoned)'
    MT_NO_BUG_JIRA_ID = 'project = ChinaUX AND issuetype = "Modification Task" and "Bug JIRA ID" is EMPTY  and status  not in (Abandoned) and "Modification Points" is not EMPTY '
    MT_NO_MODEL = 'project in (ChinaUX) AND issuetype in ("Modification Task") AND component not in (VoiceAssistant,BraviaShow,AppAssistant,"Control Proxy",KidsElder,IoT,PartnerKey,AccountApp,MySony,SonyIot,GTVS,ChinaHome) AND status not in (Abandoned)'
    MT_NO_PROJ = 'project in (ChinaUX) AND issuetype in ("Modification Task") AND component not in (Amaebi1.0DV,Amaebi1.1OTA,Amaebi2.0DV,Amaebi2.0OTA,ValUroS,Val2.2OTA,"AndroidU/T",Val2.2DV,UroQ,Amaebi2.1DV,GTVS) AND status not in (Abandoned) AND ("Submit Branch" !~ Release or "Submit Branch" is EMPTY )  AND "Pull Request Link" is not EMPTY '
    TOKYO_KEY = '"External JIRA" = "https://www.tool.sony.biz/tv-jira/browse/{0}" or "Child JIRA" = "https://www.tool.sony.biz/tv-jira/browse/{0}"'
    EXTERNAL_KEY = '"External JIRA" = "https://www.tool.sony.biz/tv-jira/browse/{0}"'
    CHILD_KEY = '"Child JIRA" = "https://www.tool.sony.biz/tv-jira/browse/{0}"'
    INTERNAL_KEY = '"Internal JIRA" = "https://www.tool.sony.biz/tv-jira/browse/{}"'
    TRD_KEY = '"3rd-party bug ID" ~ {}'


# Some fields are specific to CSC but not separated here to avoid complexity.
class FIELD:
    ID = "id"
    PROJECT = "project"
    TOTAL = "total"
    ISSUES = "issues"
    ISSUETYPE = "issuetype"
    KEY = "key"
    FIELDS = "fields"
    ASSIGNEE = "assignee"
    ISSUE_LINKS = "issuelinks"
    OUTWARD_ISSUE = "outwardIssue"
    INWARD_ISSUE = "inwardIssue"
    SUMMARY = "summary"
    PRIORITY = "priority"
    NAME = "name"
    TYPE = "type"
    VALUE = "value"
    COMPONENTS = "components"
    FIX_VERSIONS = "fixVersions"
    STATUS = "status"
    DESCRIPTION = "description"
    EXTERNAL_JIRA = "customfield_12895"
    DEVELOPER = "customfield_10420"
    TRANSITION = "transition"
    TRDID = "customfield_13660"
    CREATED = "created"
    COMMENT = "comment"
    LABELS = "labels"
    RESOLUTION = "resolution"
    IMPACT_SCOPE = "customfield_12871"
    RELEASE_JIRA_ID = "customfield_12875"
    TO_BE_INFORMED = "customfield_10406"
    TASK_JIRA_ID = "customfield_12885"
    SUBMIT_BRANCH = "customfield_12868"
    RELEASE_NOTE_LINK = "customfield_12878"
    DQA_TEST_RESULT_FILENAME = "customfield_12879"
    PULL_REQUEST = "customfield_12872"
    DQA_VERIFY_CONCLUSION = "customfield_12880"
    DUEDATE = "duedate"
    RESOLUTION = "resolution"
    RESOLUTION_DATE = "resolutiondate"
    CHANGELOG = "changelog"
    HISTORYS = "histories"
    ENVIRONMENT = "environment"
    MODIFICATION_POINTS = "customfield_12867"
    SUBTASKS = "subtasks"
    WEEKLY_REPORT = "customfield_12894"
    WORKLOG = "worklog"
    WORKLOGS = "worklogs"
    AUTHOR = "author"
    STARTED = "started"
    TIMESPENTSECONDS = "timeSpentSeconds"
    ITEMS = "items"
    TO_STRING = "toString"
    FIELD = "field"
    INTERNAL_JIRA = "customfield_14060"
    CHILD_JIRA = "customfield_14061"
    SELF = "self"
    BUG_JIRA_ID = "customfield_14062"
    FROM_STRING = "fromString"
    TO_STRING = "toString"
    DEVELOPER_TEST_RESULT_FILE_NAME = "customfield_12890"
    RESOLVED_VERSION = "customfield_10819"
    PARENT = "parent"


class FIELD_CSC(FIELD):
    RELEASED_PACKAGE_VERSION = "customfield_13260"
    DEVELOPER = "customfield_10420"
    DEFECT_RANK = "customfield_14266"
    CODE_LABELS = "customfield_12876"
    PARENT_ID = "customfield_13960"
    BOC_TEST_RESULT_FILENAME = "customfield_12882"
    BOC_VERIFY_CONCLUSION = "customfield_13170"
    BOC_VERIFY_RESULT = "customfield_12886"


class FIELD_SONY(FIELD):
    RELEASED_PACKAGE_VERSION = "customfield_29900"
    DQA_EXTERNAL_ISSUE_ID = "customfield_17000"
    DETECTED_SW_PROJECT = "customfield_38300"
    DEFECT_RANK_AUTO = "customfield_31801"
    ACTION_PLAN = "customfield_14900"
    DETECTED_VERSION = "customfield_10710"


class PROJECT:
    DQA = "CNUXBTRACK"
    CHINAUX = "ChinaUX"


class PROJECT_ID:
    CHINAUX = "11180"
    CNUXDQID = "63200"


class ISSUE_TYPE:
    BUG = "Bug"
    TASK = "Task"
    RELEASE = "Release"
    MT = "Modification Task"
    TODO = "Todo"
    SUB_TASK = "Sub-task"
    CHANGE_SPEC = '"Change Spec"'
    CHILD = "Child"


class PRIORITY:
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"
    TBD = "TBD"
    NA = "N/A"


class STATUS:
    OPEN_INTERNAL = "OPEN"
    OPEN_EXTERNAL = "Open"
    REOPENED = "Reopened"
    ASSIGNED = "Assigned"
    INVESTIGATING = "Investigating"
    REPRODUCING = "Reproducing"
    IN_PROGRESS = "IN PROGRESS"
    RESOLVED = "Resolved"
    RELEASED = "Released"
    VERIFIED = "Verified"
    CLOSED = "Closed"
    DQA_VERIFYING = "DQA Verifying"
    FL_JUDGE_DQA = "FL Judge DQA"
    BOC_VERIFYING = "BoC Verifying"
    FL_JUDGE_BOC = "FL Judge BoC"
    IMPLEMENTING = "Implementing"
    WAIT_FOR_REVIEW = "Wait for Review"
    PREPARE_FOR_SUBMIT = "Prepare for Submit"
    DEFERRED = "Deferred"


class TRANSITION:
    REOPEN = "Reopen Issue"
    RESOLVE = "Resolve Issue"
    RESOLVE_MT = "Resolve"
    ASSIGN = "Assign"
    DQA_VERIFY = "DQA Verify"
    FL_JUDGE_DQA = "FL Judge DQA"
    GO = "Go"
    FL_JUDGE_BOC = "FL Judge BoC"
    CLOSED = "Closed"
    START_PROGRESS = "Start Progress"
    APPLY_FOR_REVIEW = "Apply for Review"
    PASS = "Pass"
    RELEASED = "Released"
    CLOSE_ISSUE = "Close Issue"


class LABEL:
    TRD = "ThirdParty"
    CSC = "CSC"
    CSC_RELEASED = "CSC-Released"
    RC_RC = "RC-RC"
    RC_EXTERNAL = "RC-External"
    AUTO = "Auto"


class RESOLUTION:
    FIXED = "Fixed"
    DEFERRED = "Deferred"


class ISSUELINK:
    SYNC = "Synchronizes"
    RELATES1 = "1.Relates"
    RELATES = "Relates"
    CLONE = "Cloners"
    DUPLICATE = "Duplicate"
    BLOCK = "Blocks"
    SPLIT = "Issue split"
