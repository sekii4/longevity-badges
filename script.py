import json
import os
from datetime import date

# Read the template and check its encoding
with open("template.svg", "rb") as f:
    raw_bytes = f.read()
    print(f"File size: {len(raw_bytes)} bytes")
    print(f"First 100 bytes: {raw_bytes[:100]}")
    print()


# Try reading with different encodings
for encoding in ['utf-8', 'utf-8-sig', 'latin-1']:
    try:
        template = raw_bytes.decode(encoding)
        if "NAME" in template:
            i = template.find("NAME")
            print("FOUND 'NAME' CONTEXT:")
            print(template[i - 60:i + 60])
        else:
            print("NO 'NAME' FOUND AT ALL")

        if "__NAME__" in template:
            print(f"✓ Found {{__NAME__}} using encoding: {encoding}")
            break
        else:
            print(f"✗ {{__NAME__}} not found using encoding: {encoding}")
            # Search for NAME anywhere
            if "NAME" in template:
                print(f"  But found 'NAME' somewhere in the file")
                # Find the context around NAME
                idx = template.find("NAME")
                print(f"  Context: ...{template[max(0, idx - 20):idx + 25]}...")
    except:
        print(f"✗ Failed to decode with {encoding}")

print("\n" + "=" * 50 + "\n")

# Use utf-8-sig to handle BOM if present
template = open("template.svg", encoding="utf-8-sig").read()

polaznici = [
    {
        "name": "Marko Marković",
        "email": "marko@email.com",
        "certificate": "https://teachable.com/certificates/marko.pdf"
    }
]
os.makedirs("badges/issued", exist_ok=True)

for p in polaznici:
    slug = p["email"].replace("@", "_").replace(".", "_")

    svg = template.replace("__NAME__", p["name"])

    # Verify replacement
    if p["name"] in svg:
        print(f"✓ Successfully replaced {{__NAME__}} with {p['name']}")
    else:
        print(f"⚠ WARNING: Name replacement may have failed")

    svg_path = f"badges/issued/{slug}.svg"
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✓ Created: {svg_path}")

    badge = {
        "recipient": {
            "type": "email",
            "identity": p["email"],
            "hashed": False
        },
        "badge": {
            "name": "Longevity Degree – Foundations",
            "description": "Course completion badge",
            "image": f"https://longevity-degree.github.io/longevity-badges/{svg_path}",
            "issuer": "https://longevity.degree",
            "criteria": p["certificate"]
        },
        "issuedOn": date.today().isoformat()
    }

    json_path = f"badges/issued/{slug}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(badge, indent=2))
    print(f"✓ Created: {json_path}")

