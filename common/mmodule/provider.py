from mlogger import global_logger

from mmodule.config import Module
from mmodule.config import ModulePath

import minput
import mprint

import mmodule.config

# -------------------------------- SELECT MODULE -------------------------------------

MODULE_ID_DESCRIPTION = ["Application", "Github Code Repo"]

MODULE_LIST = mmodule.config.get_module_list()


def __select_module_id() -> int:
    # mprint.printc_description_of_item("Module Id", *MODULE_ID_DESCRIPTION)
    module_names = get_module_name_list()
    mprint.printc_choice_list(module_names)
    target = minput.input_seq_in_choice(
        "应用",
        0,
        len(MODULE_LIST) - 1,
        isExit=True,
        isSkip=False,
        isNone=False,
    )
    return target


def select_module() -> Module:
    module_id = __select_module_id()
    return get_module_by_id(module_id)


# -------------------------------- GET MODULE INFO LIST -------------------------------------


def get_module_name_list() -> list:
    return [module.name for module in MODULE_LIST]


def get_module_component_list() -> list:
    return [module.component for module in MODULE_LIST]


def get_package_name_list() -> list:
    return [module.package_name for module in MODULE_LIST]


# -------------------------------- GET INFO FROM MODULE -------------------------------------


def get_module_by_name(module_name: str) -> Module:
    for module in MODULE_LIST:
        if module_name == module.name:
            return module


def get_module_by_pacakge_name(package_name: str) -> Module:
    package_names = get_package_name_list()
    if package_name not in package_names:
        global_logger.warning(f"{package_name} not in module name list")
        return None
    module_seq = package_names.index(package_name)
    return MODULE_LIST[module_seq]


def get_module_name(module_id: int) -> str:
    return MODULE_LIST[module_id].name


def get_release_info_name(module_id: int) -> str:
    return MODULE_LIST[module_id].release_info_name


def get_test_sheet(module_id: int) -> str:
    return MODULE_LIST[module_id].test_sheet


def get_release_page_id(module_id: int) -> str:
    return MODULE_LIST[module_id].release_page_id


def get_module_path(module_id: int) -> ModulePath:
    return MODULE_LIST[module_id].module_path


def get_source_repo(module_id: int) -> str:
    return MODULE_LIST[module_id].module_path.source_repo


def get_build_path(module_id: int) -> str:
    return MODULE_LIST[module_id].module_path.get_path_build()


def get_submit_repo(module_id: int) -> str:
    return MODULE_LIST[module_id].module_path.submit_repo


def get_submit_repo_path(module_id: int) -> str:
    return MODULE_LIST[module_id].module_path.get_path_submit_repo()


def get_submit_repo_path_t6y(module_id: int) -> str:
    return MODULE_LIST[module_id].module_path.get_path_submit_repo_t6y()


def get_source_repo_path(module_id: int):
    return MODULE_LIST[module_id].module_path.get_path_source_repo()


# -------------------------------- GET MODULE FROM INFO -------------------------------------
def get_module_by_id(module_id: int) -> Module:
    return MODULE_LIST[module_id]


def get_module_by_component(component: str) -> Module:
    for module in MODULE_LIST:
        if component == module.component:
            return module


# -------------------------------- SOURCE_BRANCH -------------------------------------

MODULE_BRANCH_DESCRIPTION = ["Source Branch Name of Github Repo"]


def select_source_branch(module: Module) -> int:
    # mprint.printc_description_of_item(
    #     "Module Source Branch", *MODULE_BRANCH_DESCRIPTION
    # )
    source_branches = module.source_branch_list.get_branch_list()
    mprint.printc_choice_list(source_branches)
    target = minput.input_seq_in_choice(
        "Github代码分支",
        0,
        len(source_branches) - 1,
        isExit=True,
        isSkip=False,
        isNone=False,
    )
    return source_branches[target]


# def get_source_branch_name(module_id: int, branch_id: int) -> str:
#     branch_list = get_source_branch_list(module_id)
#     return branch_list[branch_id]


def get_supported_project_list_of_source_branch(module: Module, source_branch_name):
    assert module != None
    assert source_branch_name
    for source_branch in module.source_branch_list.source_branch_list:
        if source_branch.name == source_branch_name:
            return source_branch.project_list
    return []


# -------------------------------- TRANS -------------------------------------


def get_module_id_by_source_repo(source_repo: str):
    for module_id, module in enumerate(MODULE_LIST):
        if module.module_path.source_repo == source_repo:
            return module_id
    return None


def get_test_sheet_link_by_module_id(module_id: int):
    return MODULE_LIST[module_id].test_sheet


# -------------------------------- VERIFY -------------------------------------


def is_trd_party_module(module: Module) -> bool:
    assert module
    if module.name in ["ChinaHome", "JDSMARTHOME"]:
        return True
    return False


def is_valid_source_branch(module: Module, source_branch: str) -> bool:
    assert module
    assert source_branch
    source_branch_list = module.source_branch_list.get_branch_list()
    return source_branch in source_branch_list
