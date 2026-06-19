import json
import requests

url = "https://api.tfl.gov.uk/Line/Mode/tube"

response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()
print(json.dumps(data, indent=2))
