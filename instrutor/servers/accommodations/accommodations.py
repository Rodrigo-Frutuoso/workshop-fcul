import asyncio
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()
SERVER_NAME = "AccommodationsInfoServer"
ACCOMMODATIONS_INFO_SERVER = FastMCP(name=SERVER_NAME)

# Import dataset helpers
from servers.accommodations.helpers.airbnbs import (
    search_airbnbs_by_city,
    get_airbnbs_by_room_type,
    get_airbnbs_by_price_range,
    get_superhost_airbnbs,
    get_airbnb_statistics_by_city,
    get_available_cities as get_airbnb_cities, 
    get_airbnb_statistics_by_city
)
from servers.accommodations.helpers.hotels import (
    search_hotels_by_city,
    search_hotels_by_country,
    get_hotels_by_star_rating,
    get_hotels_by_price_range,
    get_hotels_with_offers,
    get_hotel_statistics_by_city,
    get_available_cities as get_hotel_cities,
    get_available_countries
)

# ===================== Airbnb Tools =====================

@ACCOMMODATIONS_INFO_SERVER.tool(title="search_airbnbs_by_city")
async def search_airbnbs_by_city_tool(city: str, limit: int = 50) -> dict:
    """Search for Airbnb listings by city name.

    Args:
        city (str): The name of the city to search for.
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of Airbnb listings in the specified city.
    """
    return search_airbnbs_by_city(city, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_airbnbs_by_room_type")
async def get_airbnbs_by_room_type_tool(room_type: str, limit: int = 50) -> dict:
    """Get Airbnb listings filtered by room type.

    Args:
        room_type (str): The room type to filter by (e.g., "Private room", "Entire home/apt", "Shared room").
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of Airbnb listings of the specified room type.
    """
    return get_airbnbs_by_room_type(room_type, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_airbnbs_statistics_by_city")
async def get_airbnbs_statistics_by_city_tool(city: str) -> dict:
    """Get comprehensive statistics for Airbnb listings in a specific city.

    Args:
        city (str): The name of the city to analyze.

    Returns:
        dict: Statistics including price ranges, ratings, room types, etc.
    """
    return get_airbnb_statistics_by_city(city)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_airbnbs_by_price_range")
async def get_airbnbs_by_price_range_tool(min_price: float, max_price: float, limit: int = 50) -> dict:
    """Get Airbnb listings within a specific price range.

    Args:
        min_price (float): Minimum price per night.
        max_price (float): Maximum price per night.
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of Airbnb listings within the price range.
    """
    return get_airbnbs_by_price_range(min_price, max_price, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_superhost_airbnbs")
async def get_superhost_airbnbs_tool(city: str = None, limit: int = 50) -> dict:
    """Get Airbnb listings from superhosts.

    Args:
        city (str, optional): Filter by city name.
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of Airbnb listings from superhosts.
    """
    return get_superhost_airbnbs(city, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_airbnb_statistics_by_city")
async def get_airbnb_statistics_by_city_tool(city: str) -> dict:
    """Get comprehensive statistics for Airbnb listings in a specific city.

    Args:
        city (str): The name of the city to analyze.

    Returns:
        dict: Statistics including price ranges, ratings, room types, etc.
    """
    return get_airbnb_statistics_by_city(city)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_airbnb_cities")
async def get_airbnb_cities_tool() -> dict:
    """Get list of all cities available in the Airbnb dataset.

    Returns:
        dict: List of cities with Airbnb listings.
    """
    return get_airbnb_cities()

# ===================== Hotel Tools =====================

@ACCOMMODATIONS_INFO_SERVER.tool(title="search_hotels_by_city")
async def search_hotels_by_city_tool(city: str, limit: int = 50) -> dict:
    """Search for hotel bookings by city name.

    Args:
        city (str): The name of the city to search for.
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of hotel bookings in the specified city.
    """
    return search_hotels_by_city(city, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="search_hotels_by_country")
async def search_hotels_by_country_tool(country: str, limit: int = 50) -> dict:
    """Search for hotel bookings by country name.

    Args:
        country (str): The name of the country to search for.
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of hotel bookings in the specified country.
    """
    return search_hotels_by_country(country, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_hotels_by_star_rating")
async def get_hotels_by_star_rating_tool(star_rating: int, limit: int = 50) -> dict:
    """Get hotel bookings filtered by star rating.

    Args:
        star_rating (int): The star rating to filter by (1-5).
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of hotels with the specified star rating.
    """
    return get_hotels_by_star_rating(star_rating, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_hotels_by_price_range")
async def get_hotels_by_price_range_tool(min_price: float, max_price: float, limit: int = 50) -> dict:
    """Get hotel bookings within a specific price range.

    Args:
        min_price (float): Minimum price.
        max_price (float): Maximum price.
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of hotel bookings within the price range.
    """
    return get_hotels_by_price_range(min_price, max_price, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_hotels_with_offers")
async def get_hotels_with_offers_tool(offer_category: str = None, limit: int = 50) -> dict:
    """Get hotel bookings that have special offers.

    Args:
        offer_category (str, optional): Filter by offer category (e.g., "15-50% offer").
        limit (int): Maximum number of results to return (default: 50).

    Returns:
        dict: A list of hotels with offers.
    """
    return get_hotels_with_offers(offer_category, limit)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_hotel_statistics_by_city")
async def get_hotel_statistics_by_city_tool(city: str) -> dict:
    """Get comprehensive statistics for hotel bookings in a specific city.

    Args:
        city (str): The name of the city to analyze.

    Returns:
        dict: Statistics including price ranges, star ratings, accommodation types, etc.
    """
    return get_hotel_statistics_by_city(city)

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_hotel_cities")
async def get_hotel_cities_tool() -> dict:
    """Get list of all cities available in the hotel dataset.

    Returns:
        dict: List of cities with hotel bookings.
    """
    return get_hotel_cities()

@ACCOMMODATIONS_INFO_SERVER.tool(title="get_hotel_countries")
async def get_hotel_countries_tool() -> dict:
    """Get list of all countries available in the hotel dataset.

    Returns:
        dict: List of countries with hotel bookings.
    """
    return get_available_countries()

# ===================== Combined Tools =====================

@ACCOMMODATIONS_INFO_SERVER.tool(title="compare_accommodations_by_city")
async def compare_accommodations_by_city_tool(city: str) -> dict:
    """Compare Airbnb and hotel statistics for a specific city.

    Args:
        city (str): The name of the city to compare.

    Returns:
        dict: Comparison of Airbnb and hotel statistics for the city.
    """
    airbnb_stats = get_airbnb_statistics_by_city(city)
    hotel_stats = get_hotel_statistics_by_city(city)
    
    return {
        "city": city,
        "airbnb_data": airbnb_stats,
        "hotel_data": hotel_stats
    }

async def main():
    await ACCOMMODATIONS_INFO_SERVER.run_async(
        transport="http", 
        host="localhost", 
        port=8002, 
        path="/accommodations_info_server", 
        log_level="debug"
    )

if __name__ == "__main__":
    asyncio.run(main())
