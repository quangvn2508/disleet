import datetime
from datetime import timezone

def timeToString(date: datetime):
    return date.strftime('%d %b %Y %H:%M:%S UTC')

def timestampToString(timestamp):
    return timeToString(datetime.datetime.fromtimestamp(int(timestamp), timezone.utc))

def log(msg: str):
    print(f"[{timeToString(datetime.datetime.now())}] {msg}")
