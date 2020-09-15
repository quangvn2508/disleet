import requests
from bs4 import BeautifulSoup
import time

lc = "https://leetcode.com/"

def mostRecentSubmission(username):
    # GET URL
    url = lc + username

    res = requests.get(url)

    while res.status_code == 429:
        print("Rate limited! Waiting 5 seconds")
        time.sleep(5)

        res = requests.get(url)
    
    soup = BeautifulSoup(res.text, "html.parser")

    tags = soup.find_all("div", {"class": "panel panel-default"})

    problem_list = None
    progress_list = None

    for t in tags:
        try:
            zzrot = t.find("h3", {"class": "panel-title"})
            if zzrot.text == "Most recent submissions":
                problem_list = t.find("ul", {"class": "list-group"})
            if zzrot.text == "Progress":
                progress_list = t.find("ul", {"class": "list-group"})
        except: pass
    
    if problem_list == None or progress_list == None:
        return None, -1

    problem = None
    count = 0

    # Recent problem name
    for li in problem_list:
        try:
            b = li.find("b")
            problem = b.text
            break
        except: pass

    # Problem count
    for li in progress_list:
        try:
            span = li.find("span")
            count = int(span.text.split()[0])
            break
        except: pass

    return problem, count
