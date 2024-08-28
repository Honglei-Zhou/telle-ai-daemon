import os
from datetime import timezone
import pytz
import ipinfo
from database.config import ipinfo_access_token


local_tz = pytz.timezone('America/Chicago')

dirpath = os.path.dirname(os.path.realpath(__file__))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(local_tz)


def get_ip_address(ip):
    try:
        handler = ipinfo.getHandler(ipinfo_access_token)
        details = handler.getDetails(ip)
        return details.all
    except Exception as e:
        print(e)
        return {}