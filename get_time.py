from time_format import time_format
import requests
from datetime import datetime
import pytz

def get_utc_time():
    timeapi_url = "https://www.timeapi.io/api/Time/current/zone"
    headers = {
        "Accept": "application/json",
    }
    params = {"timeZone": "etc/utc"}

    request = requests.get(timeapi_url, headers=headers, params=params)
    r_dict = request.json()
    dt = datetime(
        year=r_dict["year"],
        month=r_dict["month"],
        day=r_dict["day"],
        hour=r_dict["hour"],
        minute=r_dict["minute"],
        second=r_dict["seconds"],
        microsecond=r_dict["milliSeconds"] * 1000,
        tzinfo=pytz.UTC
    )

    return dt

def get_local_time():
    return get_utc_time().astimezone(pytz.timezone("America/Los_Angeles")).strftime(time_format)