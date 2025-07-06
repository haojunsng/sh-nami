import pandas as pd
import requests
import json
import time
from tqdm import tqdm

INPUT_CSV = "data/singapore_towns.csv"
OUTPUT_JSON = "climatact/data/towns_with_coords.json"

def get_coordinates(town):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{town}, Singapore",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "sh-nami-weather-bot" # good API citizen
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return {"lat": lat, "lon": lon}
    return None

def main():
    df = pd.read_csv(INPUT_CSV)
    towns = df.iloc[:, 0].dropna().unique()
    town_coords = {}

    for town in tqdm(towns, desc="Fetching coordinates"):
        coords = get_coordinates(town)
        if coords:
            town_coords[town.lower()] = coords
        time.sleep(1)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(town_coords, f, indent=2)

    print(f"\nSaved {len(town_coords)} towns to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
