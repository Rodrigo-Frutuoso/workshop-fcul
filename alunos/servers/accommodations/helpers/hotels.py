from typing import Optional
import os
from helpers.loader import load_dataset

HOTELS_FILENAME = "hotelbookingdata.csv"
HOTELS_HEADERS = ["addresscountryname", "city_actual", "rating_reviewcount", "center1distance", "center1label", "center2distance", "center2label", "neighbourhood", "price", "price_night", "s_city", "starrating", "rating2_ta", "rating2_ta_reviewcount", "accommodationtype", "guestreviewsrating", "scarce_room", "hotel_id", "offer", "offer_cat", "year", "month", "weekend", "holiday"]

def load_hotels() -> list[dict]:
    """
    Load all hotel booking data.
    
    Returns:
        list[dict]: List of hotel data as dictionaries.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", HOTELS_FILENAME)
    return load_dataset(dataset_path)

def search_hotels_by_city(city: str, limit: int = 50) -> dict:
    """
    Search for hotels by city name.
    
    Args:
        city (str): The city name to search for.
        limit (int): Maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the city searched, and a list of matching hotels.
    """
    city_lower = city.lower()
    hotels = load_hotels()
    matches = [h for h in hotels if city_lower in h.get("city_actual", "").lower()]
    return {
        "count": len(matches),
        "city": city,
        "hotels": matches[:limit]
    }

def search_hotels_by_country(country: str, limit: int = 50) -> dict:
    """
    Search for hotels by country name.
    
    Args:
        country (str): The country name to search for.
        limit (int): Maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the country searched, and a list of matching hotels.
    """
    country_lower = country.lower()
    hotels = load_hotels()
    matches = [h for h in hotels if country_lower in h.get("addresscountryname", "").lower()]
    return {
        "count": len(matches),
        "country": country,
        "hotels": matches[:limit]
    }

def get_hotels_by_star_rating(star_rating: int, limit: int = 50) -> dict:
    """
    Get hotels filtered by star rating.
    
    Args:
        star_rating (int): The star rating to filter by.
        limit (int): Maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the star rating searched, and a list of matching hotels.
    """
    hotels = load_hotels()
    matches = []
    for h in hotels:
        try:
            rating = int(h.get("starrating", 0))
            if rating == star_rating:
                matches.append(h)
        except (ValueError, TypeError):
            continue
    
    return {
        "count": len(matches),
        "star_rating": star_rating,
        "hotels": matches[:limit]
    }

def get_hotels_by_price_range(min_price: float, max_price: float, limit: int = 50) -> dict:
    """
    Get hotels within a price range.
    
    Args:
        min_price (float): Minimum price.
        max_price (float): Maximum price.
        limit (int): Maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the price range searched, and a list of matching hotels.
    """
    hotels = load_hotels()
    matches = []
    for h in hotels:
        try:
            price = float(h.get("price", 0))
            if min_price <= price <= max_price:
                matches.append(h)
        except (ValueError, TypeError):
            continue
    
    return {
        "count": len(matches),
        "price_range": f"{min_price}-{max_price}",
        "hotels": matches[:limit]
    }

def get_hotels_with_offers(offer_category: Optional[str] = None, limit: int = 50) -> dict:
    """
    Get hotels with offers, optionally filtered by offer category.
    
    Args:
        offer_category (Optional[str]): The offer category to filter by.
        limit (int): Maximum number of results to return.
        
    Returns:
        dict: A dictionary containing the count of matches, the offer category searched, and a list of matching hotels.
    """
    hotels = load_hotels()
    matches = []
    
    for h in hotels:
        offer = h.get("offer", "0")
        offer_cat = h.get("offer_cat", "")
        
        # Check if hotel has an offer
        try:
            has_offer = int(offer) == 1
        except (ValueError, TypeError):
            has_offer = False
        
        if has_offer:
            if offer_category:
                if offer_category.lower() in offer_cat.lower():
                    matches.append(h)
            else:
                matches.append(h)
    
    return {
        "count": len(matches),
        "offer_category": offer_category or "all",
        "hotels": matches[:limit]
    }

def get_hotel_statistics_by_city(city: str) -> dict:
    """
    Get statistics for hotels in a specific city.
    
    Args:
        city (str): The city name to get statistics for.
        
    Returns:
        dict: A dictionary containing various statistics about hotels in the specified city.
    """
    city_lower = city.lower()
    hotels = load_hotels()
    city_hotels = [h for h in hotels if city_lower in h.get("city_actual", "").lower()]
    
    if not city_hotels:
        return {"error": f"No hotels found for city: {city}"}
    
    # Calculate statistics
    prices = []
    star_ratings = []
    guest_ratings = []
    
    for h in city_hotels:
        try:
            price = float(h.get("price", 0))
            if price > 0:
                prices.append(price)
        except (ValueError, TypeError):
            pass
        
        try:
            star_rating = int(h.get("starrating", 0))
            if star_rating > 0:
                star_ratings.append(star_rating)
        except (ValueError, TypeError):
            pass
        
        try:
            guest_rating_str = h.get("guestreviewsrating", "").replace(" /5", "")
            guest_rating = float(guest_rating_str)
            if guest_rating > 0:
                guest_ratings.append(guest_rating)
        except (ValueError, TypeError):
            pass
    
    # Count by accommodation type
    accommodation_types = {}
    for h in city_hotels:
        acc_type = h.get("accommodationtype", "Unknown")
        accommodation_types[acc_type] = accommodation_types.get(acc_type, 0) + 1
    
    # Count offers
    offers_count = sum(1 for h in city_hotels if h.get("offer", "0") == "1")
    
    stats = {
        "city": city,
        "total_hotels": len(city_hotels),
        "accommodation_types": accommodation_types,
        "hotels_with_offers": offers_count
    }
    
    if prices:
        stats["price_stats"] = {
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) / len(prices)
        }
    
    if star_ratings:
        stats["star_rating_distribution"] = {}
        for rating in star_ratings:
            stats["star_rating_distribution"][rating] = stats["star_rating_distribution"].get(rating, 0) + 1
    
    if guest_ratings:
        stats["guest_rating_stats"] = {
            "min": min(guest_ratings),
            "max": max(guest_ratings),
            "avg": sum(guest_ratings) / len(guest_ratings)
        }
    
    return stats

def get_available_cities() -> dict:
    """Get list of all available cities in the hotel dataset."""
    hotels = load_hotels()
    cities = set()
    for h in hotels:
        city = h.get("city_actual", "").strip()
        if city:
            cities.add(city)
    
    return {
        "count": len(cities),
        "cities": sorted(list(cities))
    }

def get_available_countries() -> dict:
    """Get list of all available countries in the hotel dataset."""
    hotels = load_hotels()
    countries = set()
    for h in hotels:
        country = h.get("addresscountryname", "").strip()
        if country:
            countries.add(country)
    
    return {
        "count": len(countries),
        "countries": sorted(list(countries))
    }

def get_hotel_headers() -> list[str]:
    """Get the headers of the hotel dataset as a list of strings."""
    return HOTELS_HEADERS
