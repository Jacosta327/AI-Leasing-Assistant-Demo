import requests
import os
from dotenv import load_dotenv
import json

# Load credentials from .env
load_dotenv()
API_KEY = os.getenv("ENTRATA_API_KEY")
SITE = os.getenv("ENTRATA_SITE", "clsliving")
BASE_URL = f"https://apis.entrata.com/ext/orgs/{SITE}/v1/properties"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# Step 1: Get all properties
property_payload = {
    "auth": {
        "type": "apikey"
    },
    "requestId": "getProps1",
    "method": {
        "name": "getProperties",
        "params": {}
    }
}

response = requests.post(BASE_URL, headers=headers, json=property_payload)
response.raise_for_status()
properties_data = response.json()

# Corrected key path based on actual API response
result = properties_data.get("response", {}).get("result", {})
properties_block = result.get("PhysicalProperty", {})  # <-- FIXED HERE

if not properties_block or "Property" not in properties_block:
    print("❌ No properties found. Here's the full response:")
    print(json.dumps(properties_data, indent=2))
    exit()

property_list = properties_block["Property"]
property_ids = [str(p["PropertyID"]) for p in property_list]

print(f"\n✅ Retrieved {len(property_ids)} property IDs.")

# Step 2: Get websites for these properties
website_payload = {
    "auth": {
        "type": "apikey"
    },
    "requestId": "getWebsites1",
    "method": {
        "name": "getWebsites",
        "params": {
            "propertyIds": ",".join(property_ids)
        }
    }
}

response = requests.post(BASE_URL, headers=headers, json=website_payload)
response.raise_for_status()
websites_data = response.json()

# Step 3: Extract and print just the website URLs
websites = websites_data.get("response", {}).get("result", {}).get("websites", {}).get("website", [])

print("\n--- ENTRATA WEBSITE URLS ---")
if not websites:
    print("⚠️ No websites returned.")
else:
    for site in websites:
        subdomain = site.get("subdomain")
        domains = site.get("websiteDomains", {}).get("websiteDomain", [])
        for d in domains:
            domain = d.get("domain")
            # Combine subdomain + domain if needed
            if subdomain and subdomain not in domain:
                full_url = f"https://{subdomain}.{domain}"
            else:
                full_url = f"https://{domain}"
            print(full_url)
