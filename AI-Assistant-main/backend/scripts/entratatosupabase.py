import os
import json
from dotenv import load_dotenv
from supabase import create_client
from entrata_client import EntrataPartnerClient

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ENTRATA_API_KEY = os.getenv("ENTRATA_API_KEY")
ENTRATA_SITE = os.getenv("ENTRATA_SITE", "clsliving")

# Initialize Supabase + Entrata
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
entrata = EntrataPartnerClient(api_key=ENTRATA_API_KEY, site=ENTRATA_SITE)

# Fetch properties
properties_response = entrata.get_properties()
properties = (
    properties_response.get("response", {})
    .get("result", {})
    .get("PhysicalProperty", {})
    .get("Property", [])
)

print(f"🔄 Syncing {len(properties)} properties to Supabase...")

for prop in properties:
    property_id = prop["PropertyID"]
    city = prop.get("Address", {}).get("City")
    state = prop.get("Address", {}).get("State")
    data = {
        "id": property_id,
        "name": prop.get("MarketingName"),
        "lookup_code": prop.get("PropertyLookupCode"),
        "city": city,
        "state": state,
        "website": prop.get("webSite"),
    }

    supabase.table("properties").upsert(data).execute()

    # Fetch unit types for this property
    unit_response = entrata.get_unit_types(property_id)
    unit_type_list = (
        unit_response.get("response", {})
        .get("result", {})
        .get("unitTypes", {})
        .get("unitType", [])
    )

    for unit in unit_type_list:
        unit_data = {
            "id": unit["identificationType"]["idValue"],
            "property_id": property_id,
            "name": unit.get("name"),
            "bedrooms": int(unit.get("unitBedRooms", 0)),
            "bathrooms": int(unit.get("unitBathrooms", 0)),
            "min_rent": float(str(unit.get("minMarketRent", 0)).replace(",", "")),
            "max_rent": float(str(unit.get("maxMarketRent", 0)).replace(",", ""))
        }
        supabase.table("unit_types").upsert(unit_data).execute()

print("✅ Supabase sync complete.")
