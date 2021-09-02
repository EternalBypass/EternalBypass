import requests
import requests_random_user_agent

s = requests.Session()
print(s.headers['User-Agent'])

# Without a session
resp = requests.get('https://google.com')
print(resp.json()['user-agent'])
