# © Jesus A. | Proprietary and Confidential | Not for distribution or reproduction
#FOR TESTING PURPOSES ONLY
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from thefuzz import process
from utils import extract_bed_bath_request, get_timestamp
from mainSupabase import log_message  # Supabase logging
from supabase import create_client

# Load .env and clients
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# --- Load Data from Supabase ---
def load_unit_data_from_supabase():
    properties = supabase.table("properties").select("id", "name").execute().data
    units = supabase.table("unit_types").select("*").execute().data

    prop_map = {p["id"]: p["name"] for p in properties}

    records = []
    for unit in units:
        records.append({
            "property_name": prop_map.get(unit["property_id"]),
            "floorplan": unit["name"],
            "bed_bath": f'{unit["bedrooms"]} Bed / {unit["bathrooms"]} Bath',
            "price": f'${unit["min_rent"]} - ${unit["max_rent"]}',
            "move_in": "Fall 2025",  # optionally dynamic
            "available": True  # Assume all Supabase entries are current
        })

    return pd.DataFrame(records)

df = load_unit_data_from_supabase()

# --- Property Matching ---
def find_closest_property_name(user_input, df):
    matches = df['property_name'].unique()
    best_match, score = process.extractOne(user_input, matches)
    if score >= 75:
        return best_match
    return None

# --- AI Leasing Logic ---
def generate_reply(lead_message, property_name):
    matched_name = find_closest_property_name(property_name, df)
    if not matched_name:
        available_props = ", ".join(sorted(set(df['property_name'].dropna().unique())))
        return f"Sorry, we couldn't find a match for '{property_name}'. Available properties include: {available_props}"

    layout_requested = extract_bed_bath_request(lead_message)
    filtered_df = df[df['property_name'] == matched_name]

    if layout_requested:
        filtered_df = filtered_df[filtered_df['bed_bath'].str.lower() == layout_requested.lower()]

    if filtered_df.empty:
        filtered_df = df[df['property_name'] == matched_name]

    floorplans = ""
    for _, row in filtered_df.iterrows():
        floorplans += f"- Floorplan: {row['floorplan']} ({row['bed_bath']})\n  Price: {row['price']}, Move-in: {row['move_in']}, Available: {'Yes' if row['available'] else 'No'}\n\n"

    prompt = f"""
    You are a helpful, upbeat leasing assistant for a student housing property called {matched_name}. 
    You respond like you're texting a prospective resident — casual, friendly, but professional.

    A student asked: "{lead_message}"

    Here are the available floorplans at this property:
    {floorplans.strip()}

    Each floorplan is a by-the-bedroom lease. Roommate matching may be available. 
    Some units may be furnished, and utilities could be included depending on layout.

    Write your reply in 2–4 natural-sounding sentences.
    - If they asked for a specific layout (like a 3-bedroom), mention those first.
    - If none match, let them know that is not available and offer alternatives in a helpful, low-pressure way.
    - Don't say the price ranges instead say starting at the lowest price for that floorplan without decimal places.
    - Offer if they want to schedule a tour or have any other questions, but try to increase conversion.
    - When saying the property name never include the numbers for the properties. Like in "The Scarlet" not "5222 The Scarlet".
    - Don’t sound like a script — write how a real leasing manager would.

    Your tone: student-savvy, warm, helpful, not pushy.
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content.strip()

    log_interaction(lead_message, reply, matched_name)
    log_message(lead_message, reply, matched_name)

    return reply

# --- Excel Log (Optional Local Copy) ---
def log_interaction(lead_message, reply, property_name):
    log_path = "leads_log.xlsx"
    timestamp = get_timestamp()
    data = pd.DataFrame([[timestamp, property_name, lead_message, reply]],
                        columns=["Timestamp", "Property", "Lead Message", "AI Reply"])

    try:
        existing = pd.read_excel(log_path)
        updated = pd.concat([existing, data], ignore_index=True)
    except FileNotFoundError:
        updated = data

    updated.to_excel(log_path, index=False)

# --- Run in Terminal ---
if __name__ == "__main__":
    lead_msg = input("Enter a sample leasing message: ")
    prop_name = input("Which property is this for? ")
    response = generate_reply(lead_msg, prop_name)
    print("\nAI Reply:\n", response)
