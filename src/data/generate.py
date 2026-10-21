import json
import random
from pathlib import Path

random.seed(21)
vehicles = []

for i in range(50):
    vehicle = {"id" : f"V{i + 1:02d}", "w": random.randint(1, 4), "l": random.randint(2, 6), "shipping_fee": random.randint(20, 100), "weight": random.randint(5, 25), "eta": random.randint(1, 10)}

    vehicles.append(vehicle)

ship = {"w": 10, "l": 20, "max_capacity": 250}

data = {"vehicles": vehicles, "ship": ship}

folder = Path(__file__).resolve().parent
with open(folder / "data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(len(vehicles))
print(sum(v["weight"] for v in vehicles))
print(sum(v["w"] * v["l"] for v in vehicles))