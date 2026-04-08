import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Load Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Sample cleaned lead from Entrata
lead = {
    "applicant_id": 20627180,
    "customer_id": 31876366,
    "first_name": "First",
    "middle_name": "Middle",
    "last_name": "Last",
    "email": "firstlast@yahoo.com",
    "phone": "1234567891",
    "birth_date": "1990-01-01",
    "address": "1329 Test Dr",
    "city": "testing",
    "state": "AL",
    "postal_code": "79911",
    "target_move_in_date": "2025-04-15",
    "unit_occupancy_status": "vacant",
    "unit_leased_status": "leased",
    "unit_economic_status": "residential",
    "square_foot_type": "internal"
}

# Insert into Supabase
response = supabase.table("leads").insert(lead).execute()

if response.data:
    print("✅ Lead inserted successfully!")
    print(response.data)
else:
    print("❌ Error inserting lead:")
    print(response.error)
