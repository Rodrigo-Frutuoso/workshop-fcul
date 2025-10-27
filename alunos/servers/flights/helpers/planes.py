import os
from helpers.loader import load_dataset

HEADERS_PLANES = ["name","iata","icao"]
FILENAME_PLANES = "planes.dat"

def load_planes() -> list[dict]:
    """
    Load the planes dataset.

    Returns:
        list[dict]: A list of planes with their details.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", FILENAME_PLANES)
    return load_dataset(dataset_path, HEADERS_PLANES)

def find_planes_by_code(code: str) -> list[dict]:
    """Find planes by their IATA or ICAO code.
    
    Args:
        code (str): The IATA or ICAO code of the plane.
        
    Returns:
        list[dict]: A list of planes matching the code.
    """
    planes = load_planes()
    c = code.upper()
    return [p for p in planes if p.get("iata_code", "").upper() == c or p.get("icao_code", "").upper() == c]
