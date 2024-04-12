from mcommon import run_command, exit_or_continue, extract_web_link_list
from mlogger import global_logger


def show_clean_untracked_files(repo_path):
    global_logger.info("[Show Clean Untracked Files]")
    run_command(repo_path, ["git", "clean", "-nXfd"])


def clean_untracked_files(repo_path):
    global_logger.info("[Clean Untracked Files]")
    run_command(repo_path, ["git", "clean", "-Xfd"])


def show_latest_node(repo_path):
    global_logger.info("[Show Latest Node]")
    run_command(repo_path, ["git", "log", "-1"])


def reset_node_remote(repo_path, branch):
    global_logger.info("[Reset to Latest Remote Commit]")
    run_command(repo_path, ["git", "reset", "--hard", f"origin/{branch}"])


def reset_node_local(repo_path):
    global_logger.info("[Reset to Latest Local Commit]")
    run_command(repo_path, ["git", "reset", "--hard", f"^HEAD"])


def update_repo(repo_path):
    global_logger.info("[Update to Latest Node]")
    run_command(repo_path, ["git", "pull"])


def checkout_to_target_branch(repo_path, branch_name):
    global_logger.info("[Checkout to Target Branch]")
    run_command(repo_path, ["git", "checkout", branch_name])


def add_all_files(repo_path):
    global_logger.info("[Add All Files]")
    run_command(repo_path, ["git", "add", "."])


def push_to_branch(repo_path, branch):
    global_logger.info("[Push to Branch]")
    output = run_command(repo_path, ["git", "push", "origin", branch])
    web_link = extract_web_link_list(output)
    return web_link


def commit_by_txt(repo_path, txt_name):
    global_logger.info("[Commit By Txt]")
    run_command(repo_path, ["git", "commit", "-F", txt_name])


def workflow_set_up_latest_remote_node(repo_path, branch):
    global_logger.info("Fetching lateset remote node...")
    # 重置到上一次提交的节点，避免冲突
    reset_node_local(repo_path)
    # 拉取最新代码，避免目标分支在远程还没有同步到本地
    update_repo(repo_path)
    # 切换到目标分支
    checkout_to_target_branch(repo_path, branch)
    # 保证仓库为最新版本
    reset_node_remote(repo_path, branch)
    # 拉取目标分支最新代码
    update_repo(repo_path)
    # 确认当前最新的节点 //人工
    show_latest_node(repo_path)
    exit_or_continue()


# 获取Gerrit的RefsBranch
def get_refs_branch(branch):
    refs_branch = f"{branch}:refs/for/{branch}"
    return refs_branch


def workflow_submit_gerrit(repo_path, branch, txt_name):
    # 将所有文件加入缓存区
    add_all_files(repo_path)
    # 提交为节点
    commit_by_txt(repo_path, txt_name)
    # 转换成refs branch name
    refs_branch = get_refs_branch(branch)
    # 提交到目标分支
    web_link_list = push_to_branch(repo_path, refs_branch)
    gerrit_link = web_link_list[0]
    return gerrit_link
