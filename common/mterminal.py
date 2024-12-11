from mstr import ENCODE
from mlogger import global_logger

import os, subprocess

# import smbprotocol
# from smbprotocol import smb2
import platform

import mauth


# UNC path limitation: In Windows, CMD does not allow you to run commands on a UNC path (e.g., \\43.82.125.244\ChinaUX\.auto\Github_ChinaUX\SearchApp4China).
# CMD requires a mounted drive letter to run commands on a network share.


def run_command(cmd_dir: str = os.getcwd(), command=[]):
    # We use the subprocess.run() function to execute the Git command,
    # and capture the command's standard output and standard error using the capture_output=True parameter.
    # Then, we can access the standard output result via result.stdout and access standard error via result.stderr.
    # If the command fails, a subprocess.CalledProcessError exception will be raised.
    # Note that you need to be cautious when using subprocess to execute Git commands, ensuring the safety of the input parameters.
    # try:
    # Configure environment variables in the current working directory
    # os.environ["ADB"] = "F:\.dev\SDK\platform-tools"

    # Execute the Git command and capture the output
    try:
        global_logger.info(f"Running command on terminal of dir: {cmd_dir}")
        global_logger.info(f"Command: {command}]")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
            cwd=cmd_dir if cmd_dir else os.getcwd(),
            encoding=ENCODE,
            errors="replace",
        )

        # Output the command's standard error result (if any)
        if result:
            if result.stderr:
                global_logger.debug("Command error:")
                global_logger.debug(result.stderr)

            # Output the command's standard output result
            global_logger.debug("Command output:")
            global_logger.debug(result.stdout)

        execution_result = result != None and result.returncode != 0
        global_logger.info(
            "Execution result:" + "True" if execution_result else "False"
        )
    except subprocess.CalledProcessError as e:
        # Handle command execution failure
        global_logger.warning(f"Command failed with exit code: {str(e.returncode)}")
        global_logger.warning(f"Error output: {e.stderr}")
        return e.stderr


def run_to_set_java_to_11(repo_path):
    global_logger.info(f"Calling run_to_set_java_to_11 on repo_path: {repo_path}")
    return run_command(repo_path, "set JAVA_HOME=F:\.dev\JAVA\openjdk-11.0.0.1")


def run_to_set_java_to_17(repo_path):
    global_logger.info(f"Calling run_to_set_java_to_17 on repo_path: {repo_path}")
    return run_command(repo_path, "set JAVA_HOME=F:\AndroidStudio\jbr")


def run_to_assemble_apk(repo_path):
    global_logger.info(f"Calling run_to_assemble_apk on repo_path: {repo_path}")
    is_build_success = run_command(repo_path, "gradlew")
    is_assemble_success = run_command(repo_path, "gradlew assemble")
    return is_build_success and is_assemble_success


def run_to_assemble_prod_debug_apk(repo_path):
    global_logger.info(
        f"Calling run_to_assemble_prod_debug_apk on repo_path: {repo_path}"
    )
    is_build_success = run_command(repo_path, "gradlew")
    is_assemble_success = run_command(repo_path, "gradlew assembleProdDebug")
    return is_build_success and is_assemble_success


FORMAT_ARIA2C_COMMAND = "aria2c -c -x10 -k2M -s10 --check-certificate=false -d {archive_link} {download_link} --http-user=5109U25854 --http-passwd={guid_password} "


def run_to_download_sony_source(download_link: str, archive_link: str):
    global_logger.info(
        f"Calling run_to_download_sony_source on download_link: {download_link} archive_link: {archive_link}"
    )
    aria2c_command = FORMAT_ARIA2C_COMMAND.format(
        archive_link=archive_link,
        download_link=download_link,
        guid_password=mauth.GUID_PASSWORD,
    )

    # Use Popen to execute the command and capture the real-time output
    process = subprocess.Popen(
        aria2c_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        text=True,
    )

    # Read and output the real-time output of the command
    for line in process.stdout:
        print(line.strip())  # Output each line

    # Wait for the command to complete and check the return code
    process.wait()

    # Check if the command executed successfully
    download_result = process.returncode == 0
    global_logger.info("Download result:" + "True" if download_result else "False")
    return download_result


def read_txt_from_shared_docs(file_path_all: str) -> str:
    global_logger.info(
        f"Calling read_txt_from_shared_docs on file_path_all: {file_path_all}"
    )
    return run_command(os.getcwd(), ["type", file_path_all])


def set_gerrit_creditials(user: str, password: str) -> str:
    global_logger.info(
        f"Calling set_gerrit_creditials on user: {user} password: {password}"
    )
    return run_command(
        os.getcwd(),
        [
            "cmdkey",
            "/generic:https://www.tool.sony.biz",
            f"/user:{user}",
            f"/pass:{password}",
        ],
    )


def is_on_linux():
    if platform.system() == "Windows":
        return False
    elif platform.system() == "Linux":
        return True
    else:
        global_logger.error(
            "Machines other than Windows or Linux are not allowed to run the program."
        )


def setup_shared_docs_env() -> str:
    global_logger.info(f"Calling setup_shared_docs_env")
    if platform.system() == "Windows":
        if not os.path.exists("Z:\\"):
            return mount_shared_docs_on_windows()
        return True
    elif platform.system() == "Linux":
        global_logger.debug("Detected that executing machine is in Linux platform")
        global_logger.debug("setup_shared_docs_env not supported")
        return False


def mount_shared_docs_on_windows() -> str:
    global_logger.info(f"Calling mount_shared_docs_on_windows")
    network_path = r"\\43.82.125.244\ChinaUX"
    drive_letter = "Z:"
    result = subprocess.run(f"net use {drive_letter} {network_path}", shell=True)
    execution_result = result != None and result.returncode != 0
    global_logger.info("Execution result:" + "True" if execution_result else "False")
    return execution_result


def mount_shared_docs_on_windows(guid: str, password: str) -> str:
    global_logger.info(f"Calling mount_shared_docs_on_windows")
    # # 初始化 smbprotocol
    # smbprotocol.ClientConfig(username=guid, password=password)
    # smbprotocol.register_session(r"\\43.82.125.244", username=guid, password=password)
    # # 使用 SMB 协议直接访问共享路径
    # shared_path = r"\\43.82.125.244\ChinaUX"
    # file = smb2.create(shared_path, smb2.FILE_READ_DATA)
    # file.close()
