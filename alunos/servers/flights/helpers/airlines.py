import os
from utils.loader import load_dataset

HEADERS_AIRLINES = ["airline_id","name","alias","iata","icao","callsign","country","active"]
FILENAME_AIRLINES = "airlines.dat"

def load_airlines() -> list[dict]:
    """
    Load the airlines dataset.
    
    Returns:
        list[dict]: A list of airlines with their details.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", FILENAME_AIRLINES)
    return load_dataset(dataset_path, HEADERS_AIRLINES)

def find_airline_by_code(code: str) -> dict | None:
    """Find an airline by its IATA or ICAO code or name.

    Args:
        code (str): The IATA code, ICAO code, or name of the airline.

    Returns:
        dict | None: The airline data if found, else None.
    """
    
    airlines = load_airlines()
    code_upper = code.upper()
    for al in airlines:
        if al.get("iata", "").upper() == code_upper or al.get("icao", "").upper() == code_upper or al.get("name", "").lower() == code.lower():
            return al
    return None

def list_airlines_by_country(country: str) -> list[dict]:
    """List all active airlines in a given country.
    
    Args:
        country (str): The name of the country.
        
    Returns:
        list[dict]: A list of active airlines in the specified country.
    """
    airlines = load_airlines()
    c = country.lower()
    return [al for al in airlines if al.get("country", "").lower() == c and al.get("active", "Y") == "Y"]
