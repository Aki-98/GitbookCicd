import os
import re
from subprocess import PIPE
from subprocess import run
from subprocess import Popen
from subprocess import CalledProcessError
from codecs import decode

from minput import exit_or_continue
from mlogger import global_logger

PATTERN_URL = r"(https?|ftp|file)://[-A-Za-z0-9+&@#/%=~_|.:?]*[-A-Za-z0-9+&@#/%=~_|]"
PATTERN_CNJIRA = r"CHINAUX-\d+"

EXE_AAPT = "F:\\.dev\\SDK\\build-tools\\31.0.0\\aapt.exe"
EXE_NOTEPAD = "C:\\Windows\\System32\\notepad.exe"

ENCODE = "UTF-8"


def check_str_in_array(str, str_array):
    for char in str_array:
        if char in str:
            return True
    return False


def get_cnjira_set_from_str(str):
    cnjira_set = set()
    if None is str:
        return cnjira_set
    matches = re.findall(PATTERN_CNJIRA, str)
    for match in matches:
        cnjira_set.add(match)
    return cnjira_set


def is_url(str):
    if re.match(PATTERN_URL, str.strip()):
        return True
    return False


def run_command(work_directory, command):
    # 我们使用了 subprocess.run() 函数来执行 Git 命令，
    # 并通过 capture_output=True 参数来捕获命令的标准输出和标准错误。
    # 然后，我们可以通过 result.stdout 访问标准输出的结果，并通过 result.stderr 访问标准错误的结果。
    # 如果命令执行失败，将引发 subprocess.CalledProcessError 异常。
    # 请注意，使用 subprocess 执行 Git 命令时要格外小心，确保输入参数的安全性，
    # try:
    # 在当前工作目录中配置环境变量
    # os.environ["ADB"] = "F:\.dev\SDK\platform-tools"

    # 执行 Git 命令并捕获输出
    try:
        result = run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
            cwd=work_directory,
            encoding=ENCODE,
        )

        # 输出命令的标准错误结果（如果有）
        if result.stderr:
            global_logger.debug("Command error:")
            global_logger.debug(result.stderr)
            exit_or_continue()
            return result.stderr

        # 输出命令的标准输出结果
        global_logger.debug("Command output:")
        global_logger.debug(result.stdout)
        exit_or_continue()
        return result.stdout
    except CalledProcessError as e:
        # 处理命令执行失败的情况
        global_logger.warning(f"Command failed with exit code: {str(e.returncode)}")
        global_logger.warning(f"Error output: {e.stderr}")
        exit_or_continue()
        return e.stderr


def run_to_set_java_to_11(repo_path):
    global_logger.info("[Set Java to 11]")
    run_command(repo_path, "set JAVA_HOME=F:\.dev\JAVA\openjdk-11.0.0.1")


def run_to_set_java_to_17(repo_path):
    global_logger.info("[Set Java to 17]")
    run_command(repo_path, "set JAVA_HOME=F:\AndroidStudio\jbr")


def run_to_assemble_apk(repo_path):
    global_logger.info("[Build]")
    run_command(repo_path, "gradlew")
    global_logger.info("[Assemble Apk]")
    run_command(repo_path, "gradlew assemble")


def run_to_assemble_prod_debug_apk(repo_path):
    global_logger.info("[Build]")
    run_command(repo_path, "gradlew")
    global_logger.info("[Assemble Prod Debug Apk]")
    run_command(repo_path, "gradlew assembleProdDebug")


def run_to_get_app_version(path_apk):
    # 使用命令获取版本信息  aapt命令介绍可以相关博客
    get_info_command = "%s dump badging %s" % (
        EXE_AAPT,
        path_apk,
    )
    # 执行命令，并将结果以字符串方式返回
    # output = popen(get_info_command, encoding=ENCODE).read()
    p = Popen(get_info_command, stdout=PIPE, shell=True)
    # 读取输出并指定编码方式
    output, _ = p.communicate()
    output = decode(output, ENCODE)
    # 通过正则匹配，获取包名，版本号，版本名称
    match = re.compile(
        "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'"
    ).match(output)
    if not match:
        global_logger.warning(output)
        raise Exception("can't get packageinfo")
    packagename = match.group(1)
    versionCode = (int)(match.group(2))
    versionName = match.group(3)
    global_logger.info(
        " packageName: %s \n versionCode: %d \n versionName%s "
        % (packagename, versionCode, versionName)
    )
    return [versionCode, versionName]


PATTERN_WEB = r"https?://\S+"


def extract_web_link_list(str):
    str = str.strip()
    matches = re.findall(PATTERN_WEB, str)
    return matches


# 使用系统默认的文本编辑器打开文件
def edit_txt_with_vi(path_all_filename):
    os.system(f"vi {path_all_filename}")
