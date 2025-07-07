import json
from fastapi import HTTPException
from pathlib import Path
from typing import Optional, Dict

DATA_PATH = Path(__file__).parent.parent / "data" / "towns_with_coords.json"

with open(DATA_PATH, "r") as f:
    town_to_coords: Dict[str, Dict[str, float]] = json.load(f)

def get_coordinates(town_name: str) -> Optional[Dict[str, float]]:
    coords = town_to_coords.get(town_name.strip().lower())
    
    if coords:
        return coords
    else:
        raise HTTPException(status_code=404, detail=f"The town '{town_name}' isn't currently supported.")
