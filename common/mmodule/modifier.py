from mlogger import global_logger

import re


def is_valid_version_name(version_name):
    pattern = r"^\d+\.\d+\.\d+(\.\d+)?$"
    if re.match(pattern, version_name):
        global_logger.debug(f"version_name: {version_name} is valid")
        return True
    else:
        global_logger.warning(f"version_name: {version_name} not valid")
        return False


def get_version_patch(app_gradle_content: str):
    pattern = r"defaultConfig\s*{([^}]*)}"
    config_block = re.findall(pattern, app_gradle_content, re.DOTALL)[0]
    version_code_match = re.search(r"versionCode\s+(\d+)", config_block)
    version_name_match = re.search(r'versionName\s+"([^"]+)"', config_block)

    if version_code_match and version_name_match:
        version_code = version_code_match.group(1)
        version_name = version_name_match.group(1)
        return version_code, version_name
    else:
        return None, None


def write_version_path(
    path_all_app_gradle: str, version_code: str, version_name: str
) -> None:
    global_logger.debug(
        f"Alter {path_all_app_gradle} version_code to {version_code} version_name to {version_name}"
    )
    try:
        with open(path_all_app_gradle, "r", encoding="utf-8") as file:
            content = file.read()
    except IOError as e:
        global_logger.error(f"Read file error:{e}")

    version_code_match = re.search(r"versionCode\s+(\d+)", content)
    version_name_match = re.search(r'versionName\s+"([^"]+)"', content)

    content = content.replace(
        version_code_match.group(0), f"versionCode {version_code}"
    )
    content = content.replace(
        version_name_match.group(0), f'versionName "{version_name}"'
    )

    try:
        with open(path_all_app_gradle, "w", encoding="utf-8") as file:
            file.write(content)
            global_logger.info(
                f"Succeeded to write version patch: {version_code} {version_name}"
            )
    except IOError as e:
        global_logger.error(f"Write file error:{e}")


def setUpMavenSource(path_all_project_gradle: str) -> None:
    try:
        with open(path_all_project_gradle, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as e:
        global_logger.error(f"Read file error:{e}")

    keyword = "repositories {"
    insert_text = """
        maven {
            url = 'https://www.tsd.sony.biz/artifactory/libs'     // Server address
            credentials.username = 'bangguo.wang@sony.com'         // User ID
            credentials.password = 'AP27chwhLxB4xrcG53WnURkQknD8p68RkzTihE'  // Encrypted password
        }\n"""

    new_lines = []
    flag_append = False
    for line in lines:
        if flag_append:
            if "{" in line:
                num_bracket += 1
            if "}" in line:
                num_bracket -= 1
            if 0 == num_bracket:
                new_lines.append(insert_text)
                flag_append = False
        elif keyword in line:
            flag_append = True
            num_bracket = 1
        new_lines.append(line)

    try:
        with open(path_all_project_gradle, "w", encoding="utf-8") as file:
            file.writelines(new_lines)
            global_logger.info("Succeeded to set up maven source")
    except IOError as e:
        global_logger.error(f"Write file error:{e}")
