#!/usr/bin/env python3
import json, glob

all_tours = []
for fn in sorted(glob.glob("tours-*.json")):
    with open(fn) as f:
        data = json.load(f)
        all_tours.extend(data["tours"])

with open("tours.json","w") as f:
    json.dump({"tours": all_tours}, f, indent=2)
print(f"Merged {len(all_tours)} tours → tours.json")
