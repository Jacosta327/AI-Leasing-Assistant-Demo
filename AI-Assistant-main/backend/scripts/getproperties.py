import requests
import os
from dotenv import load_dotenv
import json

# Load credentials
load_dotenv()
API_KEY = os.getenv("ENTRATA_API_KEY")
SITE = os.getenv("ENTRATA_SITE", "clsliving")

# Entrata Partner API endpoint for getProperties
url = f"https://apis.entrata.com/ext/orgs/{SITE}/v1/properties"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "auth": {
        "type": "apikey"
    },
    "requestId": "getProps1",
    "method": {
        "name": "getProperties",
        "params": {}
    }
}

# Send request
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()
data = response.json()

# 🔍 Add this to inspect the full response
print(json.dumps(data, indent=2))

# Clean output (if any)
print("\n--- PROPERTY LIST ---")
for prop in data.get("data", []):
    print(f"{prop.get('name')} (ID: {prop.get('id')})")
