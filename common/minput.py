import re
from mlogger import global_logger

FIELD_SKIP = "Skip"

# -------------------------------- OPERATION -----------------------------------


def enter_or_not(operation):
    while True:
        para = input(
            f"Enter 'y' to perform operation '{operation}', enter 'n' to not operate, enter 'e' to exit the program ▶▶▶"
        )
        if para in ["Y", "y"]:
            return True
        elif para in ["n", "N"]:
            return False
        elif para in ["E", "e"]:
            exit(0)


def yn_operation(y_operation, n_operation):
    while True:
        para = input(
            f"Enter 'y' to perform '{y_operation}', \nenter 'n' to perform '{n_operation}', enter 'e' to exit the program ▶▶▶"
        )
        if para in ["Y", "y"]:
            return True
        elif para in ["n", "N"]:
            return False
        elif para in ["E", "e"]:
            exit(0)


def skip(operation):
    para = input(f"Enter 's' to skip '{operation}' ▶▶▶")
    if para in ["s", "S"]:
        return True
    else:
        return False


def exit_or_continue(message=None):
    if message:
        global_logger.warning(message)
    operation = input(
        "Enter 'e' to exit the program, enter 'any other key' to continue ▶▶▶"
    )
    if operation in ["E", "e"]:
        exit(0)
    return


def direct_exit():
    input("Enter 'any key' to exit the program ▶▶▶")
    exit(0)


# -------------------------------- INPUT -----------------------------------


def input_para(message):
    para = input(message)
    para = para.strip()
    return para


def input_para_in_pattern(message, pattern):
    para = input(message)
    para = para.strip()
    if para:
        if para in ["e", "s", "n", "q", "E", "S", "N", "Q"]:
            return para
        match = re.search(pattern, para)
        if match:
            return match.group()
        else:
            global_logger.warning(f"input does not match pattern")
            global_logger.warning(f"input > {para}")
            global_logger.warning(f"pattern > {pattern}")
    return None


def input_digit(message):
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


def input_boolean(operation_name):
    operation = enter_or_not(operation_name)
    return operation


def __format_message_in_choice(
    base_message, isExit=False, isSkip=False, isNone=False, isQuit=False
):
    message = base_message
    if isExit:
        message += ", or enter 'e' to exit the program"
    if isSkip:
        message += ", or enter 's' to skip"
    if isNone:
        message += ", or enter 'n' to write an empty value"
    if isQuit:
        message += ", or enter 'q' to complete input"
    message += " ▶▶▶"
    return message


def input_para_in_choice(
    para_name, isExit=False, isSkip=False, isNone=False, pattern=None
):
    message = f"Enter parameter '{para_name}'"
    if pattern:
        message += f", format should match {pattern}"
    message = __format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        if pattern:
            para = input_para_in_pattern(message, pattern)
        else:
            para = input_para(message)
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
    message = f"Enter multiple parameters '{para_name}'"
    if pattern:
        message += f", format should match {pattern}"
    message = __format_message_in_choice(message, isExit, isSkip, isNone, True)
    while True:
        if pattern:
            para = input_para_in_pattern(message, pattern)
        else:
            para = input_para(message)
        if isExit:
            if para in ["e", "E"]:
                exit(0)
        if isSkip:
            if para in ["s", "S"]:
                return None
        if isNone:
            if para in ["n", "N"]:
                if len(paras) != 0:
                    operation = enter_or_not(
                        "Choosing to write an empty value will clear previously entered valid data"
                    )
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
                # Check for duplicate input
                if para in paras:
                    global_logger.warning("duplicate input value")
                else:
                    paras.append(para)


def input_seq_in_choice(seq_name, min, max, isExit=False, isSkip=False, isNone=False):
    message = f"Enter sequence selection '{seq_name}', range from '{min}' to '{max}'"
    message = __format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        para = input_digit(message)
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
    message = f"Enter 月份 '{date_name}'"
    message = __format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        month = input_digit(message)
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
    message = f"Enter 日期 '{date_name}'"
    message = __format_message_in_choice(message, isExit, isSkip, isNone, False)
    while True:
        date = input_digit(message)
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
