import requests
import json
import time


url = 'https://d5dg1j9kt695d30blp03.apigw.yandexcloud.net'
apikey = "5f55e6c0-e9e5-4a9c-b313-63c01fc31460"
nickname = "grant5518"
cohort = "4"
headers = {"X-API-KEY": apikey, "X-Nickname": nickname, "X-Cohort": cohort}
method_url = '/generate_report'

r = requests.post(url + method_url, headers=headers)
response_dict = json.loads(r.content)

task_id = response_dict['task_id']

method_url = "/get_report"

time.sleep(120)
g = requests.get(f"{url}{method_url}?task_id={task_id}", headers=headers)
get_dict = json.loads(g.content)

print(get_dict)
