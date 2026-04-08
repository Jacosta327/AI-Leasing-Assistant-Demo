from mainSupabase import (get_unit_types_by_property_name)

property_name = "The Crimson"
units = get_unit_types_by_property_name(property_name)

if not units:
    reply = f"Sorry, I couldn't find any available unit types for {property_name}."
else:
    reply_lines = []
    for unit in units:
        reply_lines.append(
            f"{unit['name']}: {unit['bedrooms']} Bed / {unit['bathrooms']} Bath | ${unit['min_rent']}–${unit['max_rent']}"
        )
    reply = f"Here are the current unit types available at {property_name}:\n" + "\n".join(reply_lines)

print("\n🤖 Assistant says:")
print(reply)
