from typing import Optional
import os
from utils.loader import load_dataset

AIRBNB_FILENAME = "Aemf1.csv"
AIRBNB_HEADERS = ["City", "Price", "Day", "Room Type", "Shared Room", "Private Room", "Person Capacity", "Superhost", "Multiple Rooms", "Business", "Cleanliness Rating", "Guest Satisfaction", "Bedrooms", "City Center (km)", "Metro Distance (km)", "Attraction Index", "Normalised Attraction Index", "Restraunt Index", "Normalised Restraunt Index"]

def load_airbnbs() -> list[dict]:
    """
    Load all Airbnb data.
    
    Returns:
        list[dict]: A list of Airbnbs with their details.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", AIRBNB_FILENAME)
    return load_dataset(dataset_path)

def search_airbnbs_by_city(city: str, limit: int = 50) -> dict:
    """
    Search for Airbnbs by city name.
    
    Args:
        city (str): The name of the city to search for.
        limit (int): The maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the city name, and a list of matching Airbnbs.
    """
    city_lower = city.lower()
    airbnbs = load_airbnbs()
    matches = [a for a in airbnbs if city_lower in a.get("City", "").lower()]
    return {
        "count": len(matches),
        "city": city,
        "airbnbs": matches[:limit]
    }

def get_airbnbs_by_room_type(room_type: str, limit: int = 50) -> dict:
    """
    Get Airbnbs filtered by room type.
    
    Args:
        room_type (str): The type of room to filter by.
        limit (int): The maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the room type, and a list of matching Airbnbs.    
    """
    airbnbs = load_airbnbs()
    matches = [a for a in airbnbs if a.get("Room Type", "").lower() == room_type.lower()]
    return {
        "count": len(matches),
        "room_type": room_type,
        "airbnbs": matches[:limit]
    }

def get_airbnbs_by_price_range(min_price: float, max_price: float, limit: int = 50) -> dict:
    """
    Get Airbnbs within a price range.
    
    Args:
        min_price (float): The minimum price.
        max_price (float): The maximum price.
        limit (int): The maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the price range, and a list of matching Airbnbs.   
    """
    airbnbs = load_airbnbs()
    matches = []
    for a in airbnbs:
        try:
            price = float(a.get("Price", 0))
            if min_price <= price <= max_price:
                matches.append(a)
        except (ValueError, TypeError):
            continue
    
    return {
        "count": len(matches),
        "price_range": f"{min_price}-{max_price}",
        "airbnbs": matches[:limit]
    }

def get_superhost_airbnbs(city: Optional[str] = None, limit: int = 50) -> dict:
    """
    Get Airbnbs from superhosts, optionally filtered by city.
    
    Args:
        city (Optional[str]): The name of the city to filter by.
        limit (int): The maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the city name (or "all"), and a list of superhost Airbnbs.
    """
    airbnbs = load_airbnbs()
    matches = [a for a in airbnbs if a.get("Superhost", "").lower() == "true"]
    
    if city:
        city_lower = city.lower()
        matches = [a for a in matches if city_lower in a.get("City", "").lower()]
    
    return {
        "count": len(matches),
        "city": city or "all",
        "superhosts": matches[:limit]
    }

def get_airbnb_statistics_by_city(city: str) -> dict:
    """
    Get statistics for Airbnbs in a specific city.
    
    Args:
        city (str): The name of the city to get statistics for.
        
    Returns:
        dict: A dictionary containing various statistics about Airbnbs in the specified city.
    """
    city_lower = city.lower()
    airbnbs = load_airbnbs()
    city_airbnbs = [a for a in airbnbs if city_lower in a.get("City", "").lower()]
    
    if not city_airbnbs:
        return {"error": f"No Airbnbs found for city: {city}"}
    
    # Calculate statistics
    prices = []
    ratings = []
    satisfaction_scores = []
    
    for a in city_airbnbs:
        try:
            price = float(a.get("Price", 0))
            if price > 0:
                prices.append(price)
        except (ValueError, TypeError):
            pass
        
        try:
            rating = float(a.get("Cleanliness Rating", 0))
            if rating > 0:
                ratings.append(rating)
        except (ValueError, TypeError):
            pass
        
        try:
            satisfaction = float(a.get("Guest Satisfaction", 0))
            if satisfaction > 0:
                satisfaction_scores.append(satisfaction)
        except (ValueError, TypeError):
            pass
    
    room_types = {}
    for a in city_airbnbs:
        room_type = a.get("Room Type", "Unknown")
        room_types[room_type] = room_types.get(room_type, 0) + 1
    
    stats = {
        "city": city,
        "total_listings": len(city_airbnbs),
        "room_types": room_types
    }
    
    if prices:
        stats["price_stats"] = {
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) / len(prices)
        }
    
    if ratings:
        stats["rating_stats"] = {
            "min": min(ratings),
            "max": max(ratings),
            "avg": sum(ratings) / len(ratings)
        }
    
    if satisfaction_scores:
        stats["satisfaction_stats"] = {
            "min": min(satisfaction_scores),
            "max": max(satisfaction_scores),
            "avg": sum(satisfaction_scores) / len(satisfaction_scores)
        }
    
    return stats


def get_available_cities() -> dict:
    """
    Get list of all available cities in the Airbnb dataset.
    
    Returns:
        dict: A dictionary containing the count of unique cities and a sorted list of city names.
    """
    airbnbs = load_airbnbs()
    cities = set()
    for a in airbnbs:
        city = a.get("City", "").strip()
        if city:
            cities.add(city)
    
    return {
        "count": len(cities),
        "cities": sorted(list(cities))
    }