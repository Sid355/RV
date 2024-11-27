import requests

if 0:
    url = "https://api.upstox.com/v2/login/authorization/dialog"

    data={'client_id':'ddb1a379-62db-4ed3-b109-fb31df0596cc',
             'redirect_uri':'https://127.0.0.1:8000',
             'response_type':'code'}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=data)
    #'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id=ddb1a379-62db-4ed3-b109-fb31df0596cc&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000'
    print(response.text)
code='K_kszN'

if 1:
    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'code': code,
        'client_id': 'ddb1a379-62db-4ed3-b109-fb31df0596cc',
        'client_secret': '6j126pzt1k',
        'redirect_uri': 'https://127.0.0.1:8000',
        'grant_type': 'authorization_code',
    }

    response = requests.post(url, headers=headers, data=data)

    print(response.status_code)
    print(response.json())

    #access_token='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzM4MjExMjI5YWE2YzU3Njc4Nzk2OWEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMxNzMxNzMwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzE3OTQ0MDB9.Bzo_-XZzB6hePUaHV5IQ0lsj24BSg2fm4vbSDE6yXKY'
