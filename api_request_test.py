import requests

base_url  = 'http://localhost:5000/uppercase' 

params = {'text':'hello world'}

response = requests.get(base_url, params=params)

print(response.status_code)
print(response.json())