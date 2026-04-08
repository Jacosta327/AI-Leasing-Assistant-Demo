from supabase import create_client, Client
from dotenv import load_dotenv
import os

# © Jesus A. | Proprietary and Confidential | Not for distribution or reproduction

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_unit_types_by_property_name(property_name):
    # Step 1: Look up property by name
    prop_res = supabase.table("properties").select("id").ilike("name", f"%{property_name}%").execute()
    if not prop_res.data:
        return []

    property_id = prop_res.data[0]["id"]

    # Step 2: Get unit types for that property
    unit_res = supabase.table("unit_types").select("*").eq("property_id", property_id).execute()
    return unit_res.data

def log_message(user_message, ai_reply, property_name=None):
    data = {
        "property_name": property_name,
        "user_message": user_message,
        "ai_reply": ai_reply
    }

    return supabase.table("messages").insert(data).execute()


