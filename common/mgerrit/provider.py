from mgerrit.config import Project
import minput
import mprint

import mgerrit.config

PATTERN_PKG = r"PKG\d+(\.\d+)*"
PROJECT_DESCRIPTION = [
    "Project is associated with a particular development stage",
    "Relates to a specific submit branch of gerrit",
]

PROJECT_LIST = mgerrit.config.get_project_list()


def __select_project():
    # mprint.printc_description_of_item("Project", *PROJECT_DESCRIPTION)
    mprint.printc_choice_list(
        [project.name + " " + project.branch for project in PROJECT_LIST]
    )
    target = minput.input_seq_in_choice(
        "项目周期", 0, len(PROJECT_LIST) - 1, isExit=True, isSkip=False, isNone=False
    )
    return target


def select_project():
    project_seq = __select_project()
    project = PROJECT_LIST[project_seq]
    return project


def get_project_by_project_name(project_name: str) -> Project:
    for project in PROJECT_LIST:
        if project.name == project_name:
            return project


def get_project_by_submit_branch(submit_branch: str) -> Project:
    for project in PROJECT_LIST:
        if project.branch == submit_branch:
            return project


def get_submit_branch_by_project_name(project_name: str) -> str:
    project = get_project_by_project_name(project_name)
    return project.branch


def get_or_update_last_pkg(project: Project):
    last_pkg = project.last_pkg
    if minput.enter_or_not(f"直接使用上一个周包：{last_pkg}"):
        return last_pkg
    else:
        mprint.printc_web_link(
            f"请到PJ Common Portal查询分支 > {project.branch} 对应的PKG序号",
            "https://sonyjpn.sharepoint.com/sites/S125-132-TVSW/pjcommon/SitePages/Home.aspx",
        )
        last_pkg = minput.input_para_in_choice(
            para_name="PKG序号",
            isExit=True,
            isSkip=False,
            isNone=False,
            pattern=PATTERN_PKG,
        )


def get_project_by_fix_version(fix_version: str) -> Project:
    for project in PROJECT_LIST:
        for p_fix_version in project.fix_version_list:
            if p_fix_version == fix_version:
                return project
    return None
