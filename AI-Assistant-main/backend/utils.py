import re
from datetime import datetime

# © Jesus A. | Proprietary and Confidential | Not for distribution or reproduction

def extract_bed_bath_request(message):
    message = message.lower()

    match = re.search(r"\b(\d)x(\d)\b", message)
    if match:
        return f"{match.group(1)}x{match.group(2)}"

    bed_match = re.search(r"\b(one|two|three|four|five|six|\d)[-\s]?(bed|bdrm|bedroom)s?\b", message)
    if bed_match:
        number_map = {
            "one": "1", "two": "2", "three": "3", "four": "4",
            "five": "5", "six": "6"
        }
        digit = number_map.get(bed_match.group(1), bed_match.group(1))
        return f"{digit}x{digit}"

    if "studio" in message:
        return "studio"

    return None

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
