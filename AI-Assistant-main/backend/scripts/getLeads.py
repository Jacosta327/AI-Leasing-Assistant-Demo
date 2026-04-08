import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Entrata API setup
ENTRATA_API_KEY = os.getenv("ENTRATA_API_KEY")
URL = "https://apis.entrata.com/ext/orgs/clsliving/v1/leads"

payload = {
    "auth": {"type": "apikey"},
    "requestId": "get-leads-batch",
    "method": {
        "name": "getLeads",
        "version": "r1",
        "params": {
            "propertyId": 739676,
            "createdOnDateFrom": "04/10/2025",
            "createdOnDateTo": "04/20/2025",
            "includeDemographics": "0",
            "excludeAmenities": "1"
        }
    }
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": ENTRATA_API_KEY
}

response = requests.post(URL, headers=headers, json=payload)

print("🔍 Raw response:")
print(response.json())

if response.status_code != 200:
    print(f"❌ API failed: {response.status_code}")
    print(response.text)
    exit()

leads_data = response.json().get("response", {}).get("result", {}).get("customers", {}).get("customer", [])

if not leads_data:
    print("⚠️ No leads found.")
    exit()

inserted_count = 0

for lead in leads_data:
    try:
        address = lead.get("addresses", {}).get("address", [{}])[0]
        unit_pref = lead.get("desiredUnit", {})
        lead_entry = {
            "applicant_id": lead.get("applicantId"),
            "customer_id": lead.get("customerId"),
            "first_name": lead.get("firstName"),
            "middle_name": lead.get("middleName"),
            "last_name": lead.get("lastName"),
            "email": lead.get("email"),
            "phone": lead.get("cellPhoneNumber") or lead.get("personalPhoneNumber"),
            "birth_date": lead.get("birthDate"),
            "address": address.get("addressLine"),
            "city": address.get("city"),
            "state": address.get("state"),
            "postal_code": address.get("postalCode"),
            "target_move_in_date": lead.get("targetMoveInDate"),
            "unit_occupancy_status": unit_pref.get("unitOccupancyStatus"),
            "unit_leased_status": unit_pref.get("unitLeasedStatus"),
            "unit_economic_status": unit_pref.get("unitEconomicStatus"),
            "square_foot_type": unit_pref.get("squareFootType"),
        }
        supabase.table("leads").insert(lead_entry).execute()
        inserted_count += 1
    except Exception as e:
        print(f"❗ Failed to insert a lead: {e}")

print(f"✅ Inserted {inserted_count} leads into Supabase.")
