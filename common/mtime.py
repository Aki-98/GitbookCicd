from datetime import datetime
from pytz import timezone, utc

FORMAT_FILE_TIME = r"%Y-%m-%d_%H-%M"
FORMAT_JIRA_TAPD_TIME = r"%Y-%m-%d %H:%M"
FORMAT_DATE = r"%Y-%m-%d"
FORMAT_JIRA_WORK_LOG = r"%Y-%m-%dT%H:%M:%S.%f%z"

TIME_ZONE_TOKYO = "Asia/Tokyo"
TIME_ZONE_SHANGHAI = "Asia/Shanghai"


def convert_to_timestamp(original_time, tz=TIME_ZONE_TOKYO, format=FORMAT_FILE_TIME):
    # 先转换为native_datetime
    naive_datetime = datetime.strptime(original_time, format)
    if naive_datetime.tzinfo is None:
        # 创建带有时区信息的datetime对象
        naive_datetime = timezone(tz).localize(naive_datetime)
    # 将本地化后的时间格式化成所需的字符串
    timestamp = naive_datetime.timestamp()
    return (int)(timestamp)


def convert_to_time(original_timestamp, tz=TIME_ZONE_TOKYO, format=FORMAT_FILE_TIME):
    # print(f"[convert_to_tokyo_time] 原始时间戳：{original_timestamp}")
    # 根据时间戳创建UTC时间的datetime对象
    utc_time = datetime.fromtimestamp(original_timestamp, tz=utc)
    # 将UTC时间转换为指定时区的时间
    time_with_timezone = utc_time.astimezone(timezone(tz))
    # 格式化为字符串
    formatted_tokyo_time = time_with_timezone.strftime(format)
    # print(f"[convert_to_tokyo_time] 转换成的时间：{formatted_tokyo_time}")
    return formatted_tokyo_time


def get_current_timestamp(tz=TIME_ZONE_TOKYO):
    # 获取当前时间，并指定时区
    time = datetime.now(timezone(tz))
    # 获取时间戳（单位是秒）
    timestamp = time.timestamp()
    return (int)(timestamp)


def get_day_diff_from_timestamp(timestamp_earlier, timestamp_later):
    # 计算时间戳之间的差异（以秒为单位）
    time_difference = timestamp_later - timestamp_earlier
    # 将差异转换为天数
    days_difference = time_difference / (60 * 60 * 24)
    return days_difference


def is_same_day(timestamp1, timestamp2):
    # 转换时间戳为datetime对象
    date1 = datetime.utcfromtimestamp(timestamp1).date()
    date2 = datetime.utcfromtimestamp(timestamp2).date()
    # 比较日期部分是否相同
    return date1 == date2
