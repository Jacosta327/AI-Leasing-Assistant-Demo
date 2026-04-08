import os
import requests
from dotenv import load_dotenv

# © Jesus A. | Proprietary and Confidential | Not for distribution or reproduction

load_dotenv()

API_KEY = os.getenv("ENTRATA_API_KEY")

URL = "https://apis.entrata.com/ext/orgs/clsliving/v1/properties"

payload = {
    "auth": {
        "type": "apikey"
    },
    "requestId": "15",
    "method": {
        "name": "getFloorPlans",
        "params": {
            "propertyId": 265301,
            "usePropertyPreferences": "1",
            "includeDisabledFloorplans": "1"
        }
    }
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

response = requests.post(URL, headers=headers, json=payload)

if response.status_code == 200:
    print("✅ Floorplan data pulled successfully!")
    print(response.json())
else:
    print(f"❌ Error {response.status_code}")
    print(response.text)
