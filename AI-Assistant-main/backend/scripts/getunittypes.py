from entrata_client import EntrataPartnerClient
import os
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("ENTRATA_API_KEY")
SITE = os.getenv("ENTRATA_SITE", "clsliving")

client = EntrataPartnerClient(api_key=API_KEY, site=SITE)

property_id = 265301  # Replace if needed

result = client.get_unit_types(property_id)
print(json.dumps(result, indent=2))
