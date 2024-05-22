import requests
from datetime import datetime
import pytz

DISPLAY_TIME_FORMAT = '%m-%d-%Y %I:%M:%S %p'
GOOGLE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
GOOGLE_ZTIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
LOCAL_TZ = pytz.timezone("America/Los_Angeles")
UTC_TZ = pytz.utc

def get_utc_time():
    timeapi_url = "https://www.timeapi.io/api/Time/current/zone"
    headers = {
        "Accept": "application/json",
    }
    params = {"timeZone": "etc/utc"}

    try:
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

    except:
        print('Error getting time')
        return None

def convert_local_dt(dt):
    return LOCAL_TZ.localize(dt)

def utc_to_local(utc_dt):
    return utc_dt.astimezone(LOCAL_TZ)

def local_to_utc(local_dt):
    return local_dt.astimezone(UTC_TZ)

def disp_time(local_dt):
    return local_dt.strftime(DISPLAY_TIME_FORMAT)

def g_time(local_dt):
    return local_to_utc(local_dt).strftime(GOOGLE_ZTIME_FORMAT)

def get_date(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)