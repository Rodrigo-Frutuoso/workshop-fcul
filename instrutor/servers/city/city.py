import requests
import asyncio
from dotenv import load_dotenv
import os

from tavily import TavilyClient
from fastmcp import FastMCP

load_dotenv()

SERVER_NAME = "CityServer"
CITY_SERVER = FastMCP(name=SERVER_NAME)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@CITY_SERVER.tool(
    title="get_weather_data"
)
async def get_weather_data(city: str) -> dict:
        """
        This function is used when you need to retrieve weather information for a specified city.
        Uses OpenWeatherMap's Geocoding API to convert city name to coordinates,
        then One Call API 3.0 to get weather data.

        Args:
            city (str): The city name for which to retrieve weather data.

        Returns:
            dict: A dictionary containing weather data like temperature and weather conditions.
        """
        # Step 1: Get coordinates for the city using Geocoding API
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
        geocode_params = {
            "q": city,
            "limit": 1,
            "appid": WEATHER_API_KEY
        }
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        
        if not geocode_data:
            raise ValueError(f"City '{city}' not found")
        
        lat = geocode_data[0]['lat']
        lon = geocode_data[0]['lon']
        
        # Step 2: Get weather data using One Call API 3.0
        weather_url = "https://api.openweathermap.org/data/3.0/onecall"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "exclude": "minutely,hourly,daily,alerts"  # Only get current weather
        }
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data['current']
        return {
            "temperature": current['temp'],
            "temperature_feels_like": current['feels_like'],
            "temperature_min": current['temp'],  # Current API doesn't have min/max for current
            "temperature_max": current['temp'],  # Current API doesn't have min/max for current
            "main_condition": current['weather'][0]['main'],
            "condition_description": current['weather'][0]['description'],
        }

# @CITY_SERVER.tool(
#     title="get_trending_attractions"
# )      
# async def get_trending_attractions(city: str) -> dict:
#         """
#         This function is used when you need to retrieve trending attractions in a city.

#         Args:
#             city (str): The city name for which to retrieve trending attractions.

#         Returns:
#             dict: A dictionary containing trending attractions in the city.
#         """
        
#         client = TavilyClient(api_key=TAVILY_API_KEY)
#         response = client.search(
#             query=f"{city} trending attractions",
#             max_results=5,
#         )
        
#         return response

# @CITY_SERVER.tool(
#     title="get_time_zone"
# )
# async def get_time_zone(city: str) -> dict:
#     """
#     This function retrieves the time zone information for a specified city using Tavily's search API.

#     Args:
#         city (str): The city name for which to retrieve time zone information.

#     Returns:
#         dict: A dictionary containing time zone information for the city.
#     """
    
#     client = TavilyClient(api_key=TAVILY_API_KEY)
#     response = client.search(
#         query=f"{city} time zone",
#         max_results=1,
#     )
    
#     return response


async def main():
    # Use run_async() in async contexts
    await CITY_SERVER.run_async(transport="http", host="0.0.0.0", port=8004, path="/city_server", log_level="debug")

if __name__ == "__main__":
    # mcp.run(transport="sse", host="0.0.0.0", port=8010, path="/category_server", log_level="debug")
    asyncio.run(main())  