from mjira.const import STATUS, TRANSITION, FIELD_CSC

from mlogger import global_logger

import mjira.net
import mjira.issue


def transition_to_dqa_verifying(
    release_jira_id: str,
    status_release: str,
    release_note_link: str = None,
):
    global_logger.debug("Transition To DQA Verifying...")
    while True:
        fields = {}
        if STATUS.OPEN_INTERNAL == status_release:
            transition = TRANSITION.ASSIGN
            status_release = STATUS.ASSIGNED
        elif STATUS.ASSIGNED == status_release:
            transition = TRANSITION.DQA_VERIFY
            if release_note_link:
                fields[FIELD_CSC.RELEASE_NOTE_LINK] = release_note_link
            status_release = STATUS.DQA_VERIFYING
        else:
            return status_release
        global_logger.info(f"Next status: {status_release}")
        global_logger.info(f"data to update: {fields}")
        mjira.net.transition_csc_jira_fields(release_jira_id, transition, fields)


def transition_to_boc_verifying(
    release_jira_id: str, status_release: str, dqa_task_jira: str = None
):
    global_logger.debug("Transition To Boc Verifying...")
    while True:
        fields = {}
        if STATUS.DQA_VERIFYING == status_release:
            transition = TRANSITION.FL_JUDGE_DQA
            fields[FIELD_CSC.DQA_VERIFY_CONCLUSION] = {FIELD_CSC.VALUE: "PASS"}
            if dqa_task_jira:
                fields[FIELD_CSC.DQA_TEST_RESULT_FILENAME] = (
                    f"DQA Test Task: {mjira.issue.format_sony_jira(dqa_task_jira)}"
                )

            status_release = STATUS.FL_JUDGE_DQA
        elif STATUS.FL_JUDGE_DQA == status_release:
            transition = TRANSITION.GO
            status_release = STATUS.BOC_VERIFYING
        else:
            return status_release
        global_logger.debug(f"next status: {status_release}")
        global_logger.debug(f"data to update: {fields}")
        mjira.net.transition_csc_jira_fields(release_jira_id, transition, fields)


def transition_to_fl_judge_boc(
    release_jira_id: str,
    status_release: str,
    gerrit_link: str = None,
    boc_link: str = None,
):
    global_logger.debug("Transition To FL Judge Boc...")
    while True:
        fields = {}
        if STATUS.BOC_VERIFYING == status_release:
            transition = TRANSITION.FL_JUDGE_BOC
            fields = {}
            fields[FIELD_CSC.BOC_VERIFY_CONCLUSION] = {FIELD_CSC.VALUE: "Pass"}
            if gerrit_link:
                fields[FIELD_CSC.BOC_TEST_RESULT_FILENAME] = (
                    f"Gerrit Link: {gerrit_link}"
                )
            if boc_link:
                fields[FIELD_CSC.BOC_VERIFY_RESULT] = f"Boc Link: {boc_link}"
            status_release = STATUS.FL_JUDGE_BOC
        else:
            return status_release
        global_logger.debug(f"next status: {status_release}")
        global_logger.debug(f"data to update: {fields}")
        mjira.net.transition_csc_jira_fields(release_jira_id, transition, fields)


def trans_release_to_close(release_jira_id: str, status_release: str, weekly_pkg: str):
    global_logger.debug("Transition To Close...")
    while True:
        fields = {}
        if STATUS.FL_JUDGE_BOC == status_release:
            transition = TRANSITION.GO
            fields = {
                FIELD_CSC.RELEASED_PACKAGE_VERSION: weekly_pkg,
            }
            status_release = STATUS.RELEASED
        elif STATUS.RELEASED == status_release:
            transition = TRANSITION.CLOSED
            status_release = STATUS.CLOSED
        else:
            global_logger.info(f"release jira {release_jira_id} was closed")
            return status_release
        global_logger.info(f"next status: {status_release}")
        global_logger.info(f"data to update: {fields}")
        mjira.net.transition_csc_jira_fields(release_jira_id, transition, fields)
