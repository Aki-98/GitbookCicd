from typing import List
from dataclasses import dataclass
from mgerrit.config import Project

import mio
import mgerrit.provider

PATH_LOCAL = "D:\\.source"
PATH_REMOTE = "//43.82.125.244/ChinaUX"
PATH_MOUNT = "Z:\\"
PATH_SOURCE_REPO = "\\.auto\\Github_ChinaUX"
PATH_SUBMIT_REPO = "\\.auto\\Gerrit_ChinaUX"
PATH_SUBMIT_REPO_T6Y = "\\.auto\\Gerrit_ChinaUX_T6Y"
CONFIG_FILE = "//43.82.125.244/ChinaUX/.auto/config/modules.json"

MODULE_GITHUB_VERSION_FILE = (
    "//43.82.125.244/ChinaUX/.auto/config/module_github_version.json"
)
MODULE_GERRIT_VERSION_FILE = (
    "//43.82.125.244/ChinaUX/.auto/config/module_gerrit_version.json"
)
MODULE_TARGET_VERSION_FILE = (
    "//43.82.125.244/ChinaUX/.auto/config/module_target_version.json"
)


class FOLDER:
    RELEASE = "release"
    APP = "app"
    BUILD = "build"
    OUTPUTS = "outputs"
    APK = "apk"
    QA = "qa"
    PROD = "prod"
    RELEASE = "release"
    RELEASE_UNSIGNED = "releaseUnsigned"
    DEBUG = "debug"
    M = "M"
    T6Y = "T6Y"


class FILE:
    BUILD_GRADLE = "build.gradle"


class FLAVOR:
    DEFAULT = "default"
    PROD = "prod"
    QA = "qa"
    M = "m"
    T6Y = "t6y"


class BUILD:
    RELEASE = "release"
    DEBUG = "debug"


class DISTRIBUTION_TYPE:
    DEFAULT = "default"
    KILLSWITCH = "killswitch"
    DCS = "dcs"


class ModulePath:
    def __init__(self, source_repo, submit_repo):
        self.source_repo = source_repo
        self.submit_repo = submit_repo

    def get_path_submit_repo(self):
        return mio.join_file_path(PATH_MOUNT, PATH_SUBMIT_REPO, self.submit_repo)

    def get_path_submit_repo_remote(self):
        return mio.join_file_path_remote(
            PATH_REMOTE, PATH_SUBMIT_REPO, self.submit_repo
        )

    def get_path_submit_repo_t6y(self):
        return mio.join_file_path(PATH_MOUNT, PATH_SUBMIT_REPO_T6Y, self.submit_repo)

    def get_path_submit_repo_t6y_remote(self):
        return mio.join_file_path_remote(
            PATH_REMOTE, PATH_SUBMIT_REPO_T6Y, self.submit_repo
        )

    def get_path_source_repo(self):
        return mio.join_file_path(PATH_MOUNT, PATH_SOURCE_REPO, self.source_repo)

    def get_path_source_repo_remote(self):
        return mio.join_file_path_remote(
            PATH_REMOTE, PATH_SOURCE_REPO, self.source_repo
        )

    def get_path_all_project_gradle(self):
        return mio.join_file_path(self.get_path_source_repo(), FILE.BUILD_GRADLE)

    def get_path_all_app_gradle(self):
        # NOTE: 此处HardCode
        if not self.source_repo == "MySony4China":
            return mio.join_file_path(
                self.get_path_source_repo(), FOLDER.APP, FILE.BUILD_GRADLE
            )
        else:
            return mio.join_file_path(
                self.get_path_source_repo(), "MySony", FILE.BUILD_GRADLE
            )

    def get_path_all_app_gradle_url(self):
        # NOTE: 此处HardCode
        if not self.source_repo == "MySony4China":
            return mio.join_file_path_remote(FOLDER.APP, FILE.BUILD_GRADLE)
        else:
            return mio.join_file_path_remote("MySony", FILE.BUILD_GRADLE)

    def get_path_build(self):
        return mio.join_file_path(
            self.get_path_source_repo(),
            FOLDER.APP,
            FOLDER.BUILD,
        )

    def get_path_apk_root(self):
        return mio.join_file_path(
            self.get_path_build(),
            FOLDER.OUTPUTS,
            FOLDER.APK,
        )


@dataclass
class SourceBranch:
    name: str
    distribution_type: str
    project_list: List[Project]

    def get_distribution_tree(self):
        if self.distribution_type == DISTRIBUTION_TYPE.DEFAULT:
            return [], [BUILD.RELEASE, BUILD.DEBUG]
        elif self.distribution_type == DISTRIBUTION_TYPE.KILLSWITCH:
            return [FLAVOR.PROD, FLAVOR.QA], [BUILD.RELEASE, BUILD.DEBUG]
        elif self.distribution_type == DISTRIBUTION_TYPE.DCS:
            return [FLAVOR.M, FLAVOR.T6Y], [BUILD.RELEASE, BUILD.DEBUG]

    # def get_release_distribution(self):
    #     if self.distribution_type == DISTRIBUTION_TYPE.DEFAULT:
    #         return [BUILD.RELEASE, BUILD.DEBUG]
    #     elif self.distribution_type == DISTRIBUTION_TYPE.KILLSWITCH:
    #         return [FLAVOR.PROD, FLAVOR.QA], [BUILD.RELEASE, BUILD.DEBUG]
    #     elif self.distribution_type == DISTRIBUTION_TYPE.DCS:
    #         return [FLAVOR.M, FLAVOR.T6Y], [BUILD.RELEASE, BUILD.DEBUG]


@dataclass
class SourceBranchList:
    source_branch_list: List[SourceBranch]

    def get_branch_list(self):
        return [source_branch.name for source_branch in self.source_branch_list]


@dataclass
class Module:
    name: str  # apk name using to submit gerrit
    package_name: str
    component: str
    module_path: ModulePath
    source_branch_list: SourceBranchList
    release_info_name: str
    notice_json_name: str
    test_sheet: str
    release_page_id: str


MODULE_LIST_GLOBAL: List[Module] = []


def get_module_list() -> List[Module]:
    module_config_json = mio.get_json_from_file(file_all_path=CONFIG_FILE)
    if len(MODULE_LIST_GLOBAL) != 0:
        return MODULE_LIST_GLOBAL
    else:
        for module_name, module_info in module_config_json.items():
            module_path_item = None
            module_path_item = ModulePath(
                module_info["source_repo_name"], module_info["submit_repo_name"]
            )
            source_branch_json_list = module_info["source_branch"]
            source_branch_item_list = []
            if source_branch_json_list:
                for source_branch in source_branch_json_list:
                    project_list = []
                    for project_name in source_branch["project_list"]:
                        project = mgerrit.provider.get_project_by_project_name(
                            project_name
                        )
                        project_list.append(project)
                    source_branch_item_list.append(
                        SourceBranch(
                            name=source_branch["branch_name"],
                            distribution_type=source_branch["distribution_type"],
                            project_list=project_list,
                        )
                    )
            module_item = Module(
                name=module_name,
                package_name=module_info["package_name"],
                component=module_info["component"],
                module_path=module_path_item,
                source_branch_list=SourceBranchList(
                    source_branch_list=source_branch_item_list
                ),
                release_info_name=module_info["release_info_name"],
                notice_json_name=module_info["notice_json_name"],
                test_sheet=module_info["test_sheet"],
                release_page_id=module_info["release_page_id"],
            )
            MODULE_LIST_GLOBAL.append(module_item)
        return MODULE_LIST_GLOBAL
