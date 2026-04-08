# © Jesus A. | Proprietary and Confidential

import os
from dotenv import load_dotenv
from entrata_client import EntrataPartnerClient
from supabase import create_client

# Load credentials
load_dotenv()
API_KEY = os.getenv("ENTRATA_API_KEY")
SITE = os.getenv("ENTRATA_SITE", "clsliving")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Entrata + Supabase
entrata = EntrataPartnerClient(api_key=API_KEY, site=SITE)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get Entrata properties
properties_resp = entrata.get_properties()
property_list = (
    properties_resp.get("response", {})
    .get("result", {})
    .get("PhysicalProperty", {})
    .get("Property", [])
)

print(f"\n✅ Found {len(property_list)} properties")

# Loop and sync
for prop in property_list:
    prop_id = prop["PropertyID"]
    prop_name = prop["MarketingName"]

    # Upsert property
    supabase.table("properties").upsert({
        "id": prop_id,
        "name": prop_name
    }).execute()

    print(f"\n📍 {prop_name} (ID: {prop_id})")

    try:
        unit_types_resp = entrata.get_unit_types(prop_id)
        unit_type_list = (
            unit_types_resp.get("response", {})
            .get("result", {})
            .get("unitTypes", {})
            .get("unitType", [])
        )

        if not unit_type_list:
            print("  ⚠️ No unit types returned.")
            continue

        for unit in unit_type_list:
            data = {
                "property_id": prop_id,
                "name": unit.get("name"),
                "bedrooms": unit.get("unitBedRooms"),
                "bathrooms": unit.get("unitBathrooms"),
                "min_rent": float(str(unit.get("minMarketRent", "0")).replace(",", "")),
                "max_rent": float(str(unit.get("maxMarketRent", "0")).replace(",", ""))
            }

            supabase.table("unit_types").upsert(data).execute()

            print(f"  - {data['name']}: {data['bedrooms']} Bed / {data['bathrooms']} Bath | ${data['min_rent']}–${data['max_rent']}")

    except Exception as e:
        print(f"❌ Error fetching units for {prop_name}: {e}")
