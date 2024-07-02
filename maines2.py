import requests
import json
url = "https://api.meraki.com/api/v1/organizations"

payload = None

headers = {
    "X-Cisco-Meraki-API-Key": "75dd5334bef4d2bc96f26138c163c0a3fa0b5ca6",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
with open("./data/api2.json",'w') as files:
    response = requests.request('GET', url, headers=headers, data = payload)
    responses = response.json()
    json.dump(responses, files, indent=4, sort_keys=True)
print(response.text.encode('utf8'))

