import os
from utils.loader import load_dataset

HEADERS_COUNTRIES = ["name","iso_name","dafif_code"]
FILENAME_COUNTRIES = "countries.dat"

def load_countries() -> list[dict]:
    """Load the countries dataset.

    Returns:
        list[dict]: A list of countries with their details.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", FILENAME_COUNTRIES)
    return load_dataset(dataset_path, HEADERS_COUNTRIES)

def find_country_by_name(name: str) -> dict | None:
    """Find a country by its name.

    Args:
        name (str): The name of the country.

    Returns:
        dict | None: The country data if found, else None.
    """
    name_lower = name.lower()
    for c in load_countries():
        if c.get("name", "").lower() == name_lower:
            return c
    return None