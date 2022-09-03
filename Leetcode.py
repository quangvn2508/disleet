import requests
from utils import log

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

QUESTION_COUNT_QUERY = """
query getTotalQuestionSolved($username: String!){
    matchedUser(username: $username) {
        submitStatsGlobal {
            acSubmissionNum {
                count
            }
        }
    }
}
"""

RECENT_SOLVED_QUESTION = """
query recentAcSubmissions($username: String!, $limit: Int!) {
    recentAcSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
    }
}
"""

def post_query(query, vars):
    request = requests.post(LEETCODE_GRAPHQL, json={'query': query, 'variables': vars})
    if request.status_code == 200:
        return request.json(), 200
    else:
        return None, request.status_code

def get_total_question_solved(username: str):
    json, status_code = post_query(QUESTION_COUNT_QUERY, { "username": username })
    if json == None:
        log(f"Question count query fail with status code {status_code}, variables(username={username})")
        return None, "Unable to fetch data"

    try:
        if "errors" in json:
            return None, json["errors"][0]["message"]
        return json["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][0]["count"], None
    except Exception as e:
        log(f"Fail to parse json {str(e)} when query for total question solved, variables(username={username})")
        return None, "Exception occurred"

def get_recent_AC_submission(username: str):
    json, status_code = post_query(RECENT_SOLVED_QUESTION, { "username": username, "limit": 1 })
    if json == None:
        log(f"Recent AC query fail with status code {status_code}, variables(username={username})")
        return None, "Unable to fetch data"

    try:
        if "errors" in json:
            return None, json["errors"][0]["message"]
        return json["data"]["recentAcSubmissionList"][0], None
    except Exception as e:
        log(f"Fail to parse json {str(e)} when query for recent AC, variables(username={username})")
        return None, "Exception occurred"
