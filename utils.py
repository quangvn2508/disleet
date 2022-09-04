import datetime
from datetime import timezone

STORAGE_KEY = "leetcode_usernames"
STORAGE_NAME = "local_storage"

def timeToString(date: datetime):
    return date.strftime('%d %b %Y %H:%M:%S UTC')

def timestampToString(timestamp):
    return timeToString(datetime.datetime.fromtimestamp(int(timestamp), timezone.utc))

def log(msg: str):
    print(f"[{timeToString(datetime.datetime.now())}] {msg}")

def loadUsers():
    users = []
    with open(STORAGE_NAME, 'r') as db:
        users = db.read().split(',')
    return users

def saveUser(user):
    with open(STORAGE_NAME, 'a') as db:
        db.write(',')
        db.write(user)
