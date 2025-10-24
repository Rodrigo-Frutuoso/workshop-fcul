from typing import Optional
import os
from utils.loader import load_dataset

HEADERS_AIRPORTS = ["airport_id","name","city","country","iata","icao","latitude","longitude","altitude","timezone","dst","tz_database","type","source"]
FILENAME_AIRPORTS = "airports.dat"

def load_airports() -> list[dict]:
    """
    Load the airports dataset.
    
    Returns:
        list[dict]: A list of airports with their details.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", FILENAME_AIRPORTS)
    return load_dataset(dataset_path, HEADERS_AIRPORTS)

def find_airport_by_iata(iata: str) -> Optional[dict]:
    """
    Find an airport by its IATA code.
    
    Args: 
        iata (str): The IATA code of the airport.
        
    Returns:
        Optional[dict]: The airport data if found, else None.
    """
    iata_upper = iata.upper()
    for a in load_airports():
        if a.get("iata", "").upper() == iata_upper:
            return a
    return None

def search_airports_by_city(city: str, limit: int = 25) -> dict:
    """
    Search for airports by city name.

    Args:
        city (str): The name of the city to search for.
        limit (int): The maximum number of results to return.

    Returns:
        dict: A list of airports in the specified city.
    """
    c = city.lower()
    airports = load_airports()
    matches = [a for a in airports if c in a.get("city", "").lower()]
    return {"count": len(matches), "airports": matches[:limit]}

def list_airports_in_country(country: str, limit: int = 50) -> dict:
    """
    List all airports in a specific country.

    Args:
        country (str): The name of the country to filter airports by.
        limit (int): The maximum number of results to return.

    Returns:
        dict: A list of airports in the specified country.
    """
    c = country.lower()
    airports = load_airports()
    matches = [a for a in airports if a.get("country", "").lower() == c]
    return {"count": len(matches), "airports": matches[:limit]}
