from collections.abc import Iterable
from os import get_terminal_size
from colorama import init, Fore, Style

import unicodedata
from rich.console import Console
import json

from minput import exit_or_continue

# Initialize the colorama library
init()

# Initialize the console of rich
console = Console()

# -------------------------------- PRINT -----------------------------------


def print_dialog(*messages, color=""):
    """Print dialog box without line breaks"""
    line_width = get_terminal_size().columns - 20
    print(
        color
        + "\n\n\t+"
        + "-" * line_width
        + "+"
        + (Style.RESET_ALL if color != "" else "")
    )
    for message in messages:
        print(
            color
            + "\t| "
            + message.replace("\n", "\n\t| ")
            + (Style.RESET_ALL if color != "" else "")
        )

    # Print bottom border
    print(color + "\t+" + "-" * line_width + "+\n\n" + Style.RESET_ALL)
    exit_or_continue()


def print_dialog_split(*messages, color=""):
    """Print dialog box with line breaks"""
    line_width = get_terminal_size().columns - 20
    # Print top border
    # Only English can be used; Chinese takes up 2 spaces, but textwrap will handle it as 1 space
    print(
        color
        + "\n\n\t+"
        + "-" * line_width
        + "+"
        + (Style.RESET_ALL if color != "" else "")
    )
    # Print each message, wrapping at a fixed length
    lines = []
    for message in messages:
        line = ""
        width_count = 0
        for char in message:
            width = unicodedata.east_asian_width(char)
            if width in ("F", "W"):
                width_count += 2
            elif width in ("Na"):
                width_count += 1
            # print(width)
            line += char
            if width_count >= line_width - 3:
                lines.append(line)
                width_count = 0
                line = ""
        if line != "":
            lines.append(line)
    for line in lines:
        print(color + f"\t| {line}" + (Style.RESET_ALL if color != "" else ""))
    # Print bottom border
    print(color + "\t+" + "-" * line_width + "+\n\n" + Style.RESET_ALL)
    exit_or_continue()


def print_para(para_name, para, color=""):
    """Print parameter name and parameter value"""
    print()
    print(color + f"\t{para_name}: {para}" + Style.RESET_ALL)
    print()
    exit_or_continue()
    return para


def print_para_list(para_name, *paras, color=""):
    """Print parameter name and a list of parameter values"""
    print()
    print(color + f"\t{para_name}:" + Style.RESET_ALL)
    for para in paras:
        print(color + f"\t- {para}" + Style.RESET_ALL)
    print()
    exit_or_continue()
    return paras


def printc_confirm_method(method=None, value=None, para_name=None):
    if method:
        if value:
            results = method(value)
        else:
            results = method()
    if results:
        if (not isinstance(results, str)) and isinstance(results, Iterable):
            print_para_list(para_name, *results, Fore.YELLOW)
        else:
            print_para(para_name, results, Fore.YELLOW)
    return results


def printc_description_of_item(item_name, *message):
    formatted_para_name = f"♟{item_name}♟"
    print_para_list(formatted_para_name, *message, color=Fore.BLUE)


def printc_warning(*message):
    print_dialog_split(*message, color=Fore.RED)


def printc_web_link(link_name, link):
    print(Fore.GREEN)
    console.print(f"\t{link_name}: [link={link}]{link}[/link]")
    print(Style.RESET_ALL)
    # exit_or_continue()


def printc_choice_list(choice_list):
    target = 0
    print()
    for choice in choice_list:
        print(Fore.CYAN + f"\t『{target}』{choice}" + Style.RESET_ALL)
        target += 1
    print()


def pretty_print_json(data):
    # 将数据格式化为 JSON 字符串，使用缩进
    formatted_data = json.dumps(data, indent=4, ensure_ascii=False)

    # 定义颜色映射
    color_map = {
        '"': Fore.BLUE,  # 字符串引号为蓝色
        "{": Fore.CYAN,  # 左大括号为青色
        "}": Fore.CYAN,  # 右大括号为青色
        "[": Fore.CYAN,  # 左中括号为青色
        "]": Fore.CYAN,  # 右中括号为青色
        ":": Fore.WHITE,  # 冒号为白色
        ",": Fore.WHITE,  # 逗号为白色
        str: Fore.GREEN,  # 字符串内容为绿色
        int: Fore.YELLOW,  # 整数为黄色
        float: Fore.CYAN,  # 浮点数为青色
        bool: Fore.MAGENTA,  # 布尔值为品红色
        type(None): Fore.RED,  # None 为红色
    }

    # 将字符串分割为行以逐行处理
    lines = formatted_data.splitlines()
    colored_lines = []

    for line in lines:
        colored_line = ""
        # 逐字符处理每行
        for char in line:
            if char in color_map:
                colored_line += f"{color_map[type(char)]}{char}{Style.RESET_ALL}"
            elif isinstance(char, str) and char.strip() in ["true", "false", "null"]:
                # 为布尔值和 None 添加颜色
                colored_line += f"{color_map[char.strip()]}{char}{Style.RESET_ALL}"
            else:
                colored_line += char
        colored_lines.append(colored_line)

    # 输出彩色的 JSON 字符串
    print("\n".join(colored_lines))
