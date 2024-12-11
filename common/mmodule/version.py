import mio
import mmodule.config

PATTERN_VERSION_CODE = r"\d+"
PATTERN_VERSION_NAME = r"^\d+\.\d+\.\d+(\.\d+)?$"

TARGET_VERSION_JSON_CONFIG = None
GERRIT_VERSION_JSON_CONFIG = None


def get_target_version_dict(module_name: str, source_branch_name: str):
    assert module_name
    assert source_branch_name
    global TARGET_VERSION_JSON_CONFIG
    if not TARGET_VERSION_JSON_CONFIG:
        TARGET_VERSION_JSON_CONFIG = mio.get_json_from_file(
            mmodule.config.MODULE_TARGET_VERSION_FILE
        )
    target_range_dict = TARGET_VERSION_JSON_CONFIG[module_name][source_branch_name]
    return target_range_dict


def get_gerrit_version_patch(module_name: str, branch: str):
    assert module_name
    assert branch
    global GERRIT_VERSION_JSON_CONFIG
    if not GERRIT_VERSION_JSON_CONFIG:
        GERRIT_VERSION_JSON_CONFIG = mio.get_json_from_file(
            mmodule.config.MODULE_GERRIT_VERSION_FILE
        )
    module_project_info_list = GERRIT_VERSION_JSON_CONFIG[module_name]
    for project_info in module_project_info_list:
        if project_info and project_info["project_branch"] == branch:
            return project_info["version_code"], project_info["version_name"]


def accumulate_version_patch(version_code: str, version_name: str):
    assert version_code
    assert version_name
    target_version_code = (int)(version_code) + 1
    if "alpha" in version_name:
        version_name = version_name.split(".alpha")[0]
    major, minor, patch = map(int, version_name.split("."))
    patch += 1
    target_version_name = f"{major}.{minor}.{patch}"
    return (str)(target_version_code), target_version_name


def is_version_in_range(
    target_version_dict: dict,
    version_code: str,
    version_name: str,
) -> bool:
    assert target_version_dict
    assert version_code
    assert version_name

    min_version_code = target_version_dict["min_version_code"]
    max_version_code = target_version_dict["max_version_code"]
    min_version_name = target_version_dict["min_version_name"]
    max_version_name = target_version_dict["max_version_name"]

    if not (min_version_code <= int(version_code) <= max_version_code):
        return False

    major, minor, patch = map(int, version_name.split("."))
    major_min, minor_min, patch_min = map(int, min_version_name.split("."))
    major_max, minor_max, patch_max = map(int, max_version_name.split("."))

    if not (major_min <= major <= major_max):
        return False
    if not (minor_min <= minor <= minor_max):
        return False
    if not (patch_min <= patch <= patch_max):
        return False

    return True
