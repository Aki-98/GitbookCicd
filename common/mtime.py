from datetime import datetime
from pytz import timezone, utc

FORMAT_FILE_TIME = r"%Y-%m-%d_%H-%M"
FORMAT_TAPD = r"%Y-%m-%d %H:%M"
FORMAT_DATE = r"%Y-%m-%d"
FORMAT_DATE_OF_MONTH = r"%m/%d"
FORMAT_JIRA = r"%Y-%m-%dT%H:%M:%S.%f%z"
FORMAT_DATE_YEAR_FIRST = r"%Y/%m/%d"
FORMAT_DATE_YEAR_END = r"%m/%d/%Y"
FORMAT_GIT = r"%Y-%m-%d %H:%M:%S %z"

TIME_ZONE_TOKYO = "Asia/Tokyo"
TIME_ZONE_SHANGHAI = "Asia/Shanghai"


def convert_to_timestamp(original_time, tz=TIME_ZONE_TOKYO, format=FORMAT_FILE_TIME):
    # First convert to native_datetime
    naive_datetime = datetime.strptime(original_time, format)
    if naive_datetime.tzinfo is None:
        # Create a datetime object with timezone information
        naive_datetime = timezone(tz).localize(naive_datetime)
    # Format the localized time into the required string
    timestamp = naive_datetime.timestamp()
    return (int)(timestamp)


def convert_to_time(original_timestamp, tz=TIME_ZONE_TOKYO, format=FORMAT_FILE_TIME):
    # print(f"[convert_to_tokyo_time] Original timestamp: {original_timestamp}")
    # Create a datetime object for UTC time based on the timestamp
    utc_time = datetime.fromtimestamp(original_timestamp, tz=utc)
    # Convert UTC time to the specified timezone
    time_with_timezone = utc_time.astimezone(timezone(tz))
    # Format as a string
    formatted_tokyo_time = time_with_timezone.strftime(format)
    # print(f"[convert_to_tokyo_time] Converted time: {formatted_tokyo_time}")
    return formatted_tokyo_time


def convert_str_to_datetime(date_str: str, format: str):
    dt = datetime.strptime(date_str.strip(), format)
    return dt


def convert_datetime_to_str(dt: datetime, format: str):
    date_str = dt.strftime(format)
    return date_str


def get_current_timestamp(tz=TIME_ZONE_TOKYO):
    # Get the current time and specify the timezone
    time = datetime.now(timezone(tz))
    # Get the timestamp (in seconds)
    timestamp = time.timestamp()
    return (int)(timestamp)


def get_current_datetime(tz=TIME_ZONE_TOKYO):
    return datetime.now(timezone(tz))


def get_current_time_of_minus():
    # Get the current date
    current_date = datetime.now()
    # Format the current date as month/day
    formatted_date = current_date.strftime(FORMAT_TAPD)
    return formatted_date


def get_current_time_of_month():
    # Get the current date
    current_date = datetime.now()
    # Format the current date as month/day
    formatted_date = current_date.strftime(r"%m/%d")
    return formatted_date


def get_current_time_of_year(format=FORMAT_DATE_YEAR_END):
    # Get the current date
    current_date = datetime.now()
    # Format the current date as month/day
    formatted_date = current_date.strftime(format)
    return formatted_date


def get_day_diff_from_timestamp(timestamp_earlier, timestamp_later):
    # Calculate the difference between timestamps (in seconds)
    time_difference = timestamp_later - timestamp_earlier
    # Convert the difference to days
    days_difference = time_difference / (60 * 60 * 24)
    return days_difference


def get_timestamp_after_days(original_timestamp: int, days: int):
    # Calculate the number of seconds in the given number of days
    seconds_in_days = days * 60 * 60 * 24
    # Add the calculated seconds to the original timestamp
    new_timestamp = original_timestamp + seconds_in_days
    return new_timestamp


def is_same_day(timestamp1, timestamp2):
    # Convert timestamps to datetime objects
    date1 = datetime.utcfromtimestamp(timestamp1).date()
    date2 = datetime.utcfromtimestamp(timestamp2).date()
    # Compare if the date parts are the same
    return date1 == date2
