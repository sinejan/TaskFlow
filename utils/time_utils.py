from datetime import datetime

def str_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M")

def now():
    return datetime.now()
