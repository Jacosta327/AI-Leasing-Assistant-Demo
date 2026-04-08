import requests

class EntrataPartnerClient:
    def __init__(self, api_key, site):
        self.api_key = api_key
        self.site = site
        self.base_url = f"https://apis.entrata.com/ext/orgs/{site}/v1"

    def _call(self, method_name, params=None, request_id="1"):
        if params is None:
            params = {}

        resource_map = {
            "getProperties": "properties",
            "getVendors": "vendors",
            "getUnits": "units",
            "getLeads": "leads",
            "getLeases": "leases",
            "getUnitTypes": "propertyunits",
            # add more as needed
        }
        resource_path = resource_map.get(method_name, "")
        url = f"{self.base_url}/{resource_path}"

        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "auth": {
                "type": "apikey"
            },
            "requestId": request_id,
            "method": {
                "name": method_name,
                "params": params
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_properties(self):
        return self._call("getProperties", request_id="getProps")

    def get_units(self, property_id):
        return self._call("getUnits", params={"propertyId": property_id}, request_id=f"units-{property_id}")

    def get_unit_types(self, property_id):
        return self._call("getUnitTypes", params={"propertyId": property_id}, request_id=f"unitTypes-{property_id}")

