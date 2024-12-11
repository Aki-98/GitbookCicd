import re
import os

PATTERN_URL = r"(https?|ftp|file)://[-A-Za-z0-9+&@#/%=~_|.:?]*[-A-Za-z0-9+&@#/%=~_|]"
PATTERN_WEB = r"https?://\S+"
PATTERN_CNJIRA = r"CHINAUX-\d+"

ENCODE = "UTF-8"
PATTERN_BRACKET_EN = r"\[(.*?)\]"
PATTERN_BRACKET_CN = r"\【(.*?)\】"


def check_str_in_array(str, str_array):
    if str:
        for char in str_array:
            if char in str:
                return True
        return False
    else:
        return False


def is_url(str):
    if re.match(PATTERN_URL, str.strip()):
        return True
    return False


def extract_web_link_list(str):
    str = str.strip()
    matches = re.findall(PATTERN_WEB, str)
    return matches


def remove_extra_newlines(text):
    # Use regular expressions to replace consecutive newlines with a single newline
    return re.sub(r"\n+", "\n", text)


def extract_model(summary):
    matches = re.findall(PATTERN_BRACKET_EN, summary)
    matches += re.findall(PATTERN_BRACKET_CN, summary)
    return matches


def extract_summary_title(content):
    result = re.sub(r"\[.*?\]", "", content).strip()
    return result


# ---------------- PULL REQUEST ----------------

PATTERN_PULL_REQUEST = r"https://github\.com/[^/]+/[^/]+/pull/\d+"
PATTERN_PULL_REQUEST_INFO = r"https://github.com/([^/]+)/([^/]+)/pull/(\d+)"


def extract_pr_list(url: str):
    matches = re.findall(PATTERN_PULL_REQUEST, url)
    return matches


def extract_pr_info(text: str):
    # Use re.match to match the pattern
    match = re.match(PATTERN_PULL_REQUEST_INFO, text)

    if match:
        # If the match is successful, extract organization, repository, and PR number
        org = match.group(1)
        repo = match.group(2)
        pr_number = match.group(3)
        return org, repo, pr_number
    else:
        # If the match fails, return None
        return None


def extract_pr_num(text: str):
    org, repo, pr_number = extract_pr_info(text)
    return pr_number


def extract_commit_type(text: str):
    match = re.search(r"(\w+)\(.*?\):", text)

    if match:
        action = match.group(1)
        return action


def extract_tag_name(release_note_url: str):
    match = re.search(r"/tag/([^/]+)$", release_note_url)

    if match:
        tag_name = match.group(1)
        return tag_name


def safe_increment_string_number(input_str):
    try:
        # Try to convert the string to an integer
        number = int(input_str)
        # Increment the integer by one
        number += 1
        # Convert the result back to a string and return it
        return str(number)
    except ValueError:
        # If the input string cannot be converted to an integer, return an error message or handle it
        return print("Input is not a valid integer")


def is_four_digit_number(s):
    # Check if s is None
    if s is None:
        return False
    # Check if the string length is 4 and all characters are digits
    return len(s) == 4 and s.isdigit()


def fuzzy_match(str1, str2):
    # Create a 2D array to store the computation results
    dp = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]

    # Initialize boundary values
    for i in range(len(str1) + 1):
        dp[i][0] = i
    for j in range(len(str2) + 1):
        dp[0][j] = j

    # Fill the dynamic programming table
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Characters are the same, cost is 0
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # Deletion
                    dp[i][j - 1],  # Insertion
                    dp[i - 1][j - 1],
                )  # Substitution

    # Calculate the Levenshtein distance
    distance = dp[-1][-1]

    # Convert to similarity, ranging from 0 to 1
    max_len = max(len(str1), len(str2))
    similarity = 1 - (distance / max_len)
    return similarity


def extract_dependencies_from_gradle(gradle_text: str) -> list:
    # Define regex patterns for various dependency formats
    patterns = [
        # Matches "implementation 'group:artifact:version'"
        r"implementation\s+'([\w\.\-]+):([\w\.\-]+):([\w\.\-]+)'",
        # Matches "implementation name: 'library-name', ext: 'aar'"
        r"implementation\s*\(name:\s*\"([\w\.\-]+)\",\s*ext:\s*'([\w]+)'\)",
        # Matches "implementation files('libs/library.jar')"
        r"implementation\s+files?\(\s*'([^']+)'",
        # Matches "implementation 'group:artifact:version'"
        r'implementation\s+"([\w\.\-]+):([\w\.\-]+):([\w\.\-]+)"',
        # Matches "api 'group:artifact:version'"
        r"api\s+'([\w\.\-]+):([\w\.\-]+):([\w\.\-]+)'",
    ]

    dependencies = []

    # Iterate through each line to find dependencies
    for line in gradle_text.splitlines():
        line = line.strip()
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                if len(match.groups()) == 3:
                    # Grouped format 'group:artifact:version'
                    group, artifact, version = match.groups()
                    dependencies.append(
                        {"library": f"{group}:{artifact}", "version": version}
                    )
                elif len(match.groups()) == 2:
                    # name format 'name: "library-name", ext: "aar"'
                    name, ext = match.groups()
                    dependencies.append({"library": name, "extension": ext})
                elif len(match.groups()) == 1:
                    # file path format
                    file_path = match.group(1)
                    dependencies.append({"library": file_path, "type": "file"})

    return dependencies


import string
import random

CHARACTERS_ALPHANUMERIC = string.ascii_letters + string.digits


def generate_random_alphanumeric(length=11):
    random_string = "".join(
        random.choice(CHARACTERS_ALPHANUMERIC) for _ in range(length)
    )
    return random_string


PATTERN_ALPHANUMERIC = r"^[a-zA-Z0-9]{11}$"


def is_valid_alphanumeric(file_path: str) -> bool:
    import mio

    file_basename = mio.get_basename(file_path)
    return bool(re.match(PATTERN_ALPHANUMERIC, file_basename))
