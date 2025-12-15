import json
from datetime import date

template = open("badge-template.svg", encoding="utf-8").read()

polaznici = [
  {
    "name": "Marko Marković",
    "email": "marko@email.com",
    "certificate": "https://teachable.com/certificates/marko.pdf"
  }
]

for p in polaznici:
    slug = p["email"].replace("@", "_").replace(".", "_")

    svg = template.replace("{{NAME}}", p["name"])
    svg_path = f"badges/issued/{slug}.svg"
    open(svg_path, "w", encoding="utf-8").write(svg)

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
    open(json_path, "w", encoding="utf-8").write(json.dumps(badge, indent=2))
