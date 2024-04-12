import re
from mlogger import global_logger

FIELD_SKIP = "Skip"

# -------------------------------- OPERATION -----------------------------------


def enter_or_not(operation):
    while True:
        para = input(f"输入『y』进行操作『{operation}』, 或输入『n』不操作 ▶▶▶")
        if para in ["Y", "y"]:
            return True
        elif para in ["n", "N"]:
            return False


def skip(operation):
    para = input(f"输入『s』跳过『{operation}』▶▶▶")
    if para in ["s", "S"]:
        return True
    else:
        return False


def exit_or_continue(message=None):
    if message:
        global_logger.warning(message)
    operation = input("输入『e』结束程序, 输入『其他键』继续执行 ▶▶▶")
    if operation in ["E", "e"]:
        exit(0)
    return


def direct_exit():
    input("输入『任意键』结束程序 ▶▶▶")
    exit(0)


# -------------------------------- INPUT -----------------------------------


def _input_para(message):
    para = input(message)
    para = para.strip()
    return para


def _input_para_in_pattern(message, pattern):
    para = input(message)
    para = para.strip()
    if para:
        if para in ["e", "s", "n", "q", "E", "S", "N", "Q"]:
            return para
        match = re.search(pattern, para)
        if match:
            return match.group()
        else:
            global_logger.warning("input does not match format")
    return None


def _input_digit(message):
    para = input(message)
    para = para.strip()
    if para:
        if para in ["e", "s", "n", "q", "E", "S", "N", "Q"]:
            return para
        if para.isdigit():
            seq = (int)(para)
            return seq
        else:
            global_logger.warning("not a num")
    return None


def _input_boolean(operation_name):
    operation = enter_or_not(operation_name)
    return operation


def _format_message_in_choice(
    base_messgae, isExit=False, isSkip=False, isNone=False, isQuit=False
):
    message = base_messgae
    if isExit:
        message += ", 或输入『e』结束程序"
    if isSkip:
        message += ", 或输入『s』跳过"
    if isNone:
        message += ", 或输入『n』写入空值"
    if isQuit:
        message += ", 或输入『q』完成输入"
    message += " ▶▶▶"
    return message


def input_para_in_choice(
    para_name, isExit=False, isSkip=False, isNone=False, pattern=None
):
    message = f"输入参数『{para_name}』"
    if pattern:
        message += f", 格式应符合{pattern}"
    message = _format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        if pattern:
            para = _input_para_in_pattern(message, pattern)
        else:
            para = _input_para(message)
        if para:
            if isExit:
                if para in ["e", "E"]:
                    exit(0)
            if isSkip:
                if para in ["s", "S"]:
                    return None
            if isNone:
                if para in ["n", "N"]:
                    return FIELD_SKIP
            return para


def input_paras_in_choice(
    para_name, isExit=False, isSkip=False, isNone=False, pattern=None
):
    paras = []
    message = f"输入多个参数『{para_name}』"
    if pattern:
        message += f", 格式应符合{pattern}"
    message = _format_message_in_choice(message, isExit, isSkip, isNone, True)
    while True:
        if pattern:
            para = _input_para_in_pattern(message, pattern)
        else:
            para = _input_para(message)
        if isExit:
            if para in ["e", "E"]:
                exit(0)
        if isSkip:
            if para in ["s", "S"]:
                return None
        if isNone:
            if para in ["n", "N"]:
                if len(paras) != 0:
                    operation = enter_or_not("选择写入空值将清除之前输入的有效数据")
                    if not operation:
                        continue
                return FIELD_SKIP
        if para in ["q", "Q"]:
            if paras:
                return paras
            else:
                global_logger.warning("haven't input a valid data")
        else:
            if para:
                # 检查是否重复输入
                if para in paras:
                    global_logger.warning("duplicate input value")
                else:
                    paras.append(para)


def input_seq_in_choice(seq_name, min, max, isExit=False, isSkip=False, isNone=False):
    message = f"输入序号选择『{seq_name}』, 范围为『{min}』到『{max}』"
    message = _format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        para = _input_digit(message)
        if para or para == 0:
            if isinstance(para, int):
                if para in range(min, max + 1):
                    return para
                else:
                    global_logger.warning("not a num in range")
                    continue
            if isExit:
                if para in ["e", "E"]:
                    exit(0)
            if isSkip:
                if para in ["s", "S"]:
                    return None
            if isNone:
                if para in ["n", "N"]:
                    return FIELD_SKIP


def input_date_in_choice(date_name, isExit=False, isSkip=False, isNone=False):
    message = f"输入月份『{date_name}』"
    message = _format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        month = _input_digit(message)
        if isinstance(month, int):
            if month in range(1, 13):
                break
            else:
                global_logger.warning("not a num of month")
                continue
        if month in ["e", "E"]:
            exit(0)
        if month in ["s", "S"]:
            return None
        if month in ["n", "N"]:
            return FIELD_SKIP
    message = f"输入日期『{date_name}』"
    message = _format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        date = _input_digit(message)
        if isinstance(date, int):
            if date in range(1, 32):
                break
            else:
                global_logger.warning("not a num of date")
                continue
        if date in ["e", "E"]:
            exit(0)
        if date in ["s", "S"]:
            return None
        if date in ["n", "N"]:
            return FIELD_SKIP
    return f"2024-{month}-{date}"
