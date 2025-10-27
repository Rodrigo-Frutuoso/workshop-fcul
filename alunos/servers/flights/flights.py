import asyncio
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()
SERVER_NAME = "FlightsInfoServer"
FLIGHTS_INFO_SERVER = FastMCP(name=SERVER_NAME)

# Import dataset helpers
from helpers.airports import find_airport_by_iata, search_airports_by_city, list_airports_in_country
from helpers.airlines import find_airline_by_code, list_airlines_by_country
from helpers.routes import destinations_from_airport, find_route_paths
from helpers.planes import find_planes_by_code 
from helpers.countries import find_country_by_name

# ===================== Tools =====================

@FLIGHTS_INFO_SERVER.tool(title="get_airport_by_iata")
async def get_airport_by_iata(iata: str) -> dict:
    """Get airport information by IATA code.

    Args:
        iata (str): The IATA code of the airport.

    Returns:
        dict: The airport information or an error message.
    """
    airport = find_airport_by_iata(iata)
    return {"airport": airport} if airport else {"error": f"No airport found with IATA code {iata}"}

@FLIGHTS_INFO_SERVER.tool(title="search_airports_by_city")
async def search_airports_by_city_tool(city: str) -> dict:
    """Search for airports by city name.

    Args:
        city (str): The name of the city to search for.

    Returns:
        dict: A list of airports in the specified city.
    """
    return search_airports_by_city(city)

@FLIGHTS_INFO_SERVER.tool(title="list_airports_in_country")
async def list_airports_in_country_tool(country: str) -> dict:
    """List all airports in a specific country.

    Args:
        country (str): The name of the country to filter airports by.

    Returns:
        dict: A list of airports in the specified country.
    """
    return list_airports_in_country(country)

@FLIGHTS_INFO_SERVER.tool(title="get_airline_by_code")
async def get_airline_by_code_tool(code: str) -> dict:
    """Get airline information by IATA or ICAO code or name.

    Args:
        code (str): The IATA code, ICAO code, or name of the airline.

    Returns:
        dict: The airline information or an error message.
    """
    airline = find_airline_by_code(code)
    return {"airline": airline} if airline else {"error": f"Airline not found for code/name {code}"}

@FLIGHTS_INFO_SERVER.tool(title="list_airlines_by_country")
async def list_airlines_by_country_tool(country: str) -> dict:
    """List all airlines in a specific country.

    Args:
        country (str): The name of the country to filter airlines by.

    Returns:
        dict: A list of airlines in the specified country.
    """
    airlines = list_airlines_by_country(country)
    return {"count": len(airlines), "airlines": airlines}

@FLIGHTS_INFO_SERVER.tool(title="get_routes_from_airport")
async def get_routes_from_airport_tool(source_iata: str) -> dict:
    """Get all routes from a specific airport.

    Args:
        source_iata (str): The IATA code of the source airport.

    Returns:
        dict: A list of routes from the specified airport.
    """
    destinations = destinations_from_airport(source_iata)
    return {"source": source_iata.upper(), "destinations_count": len(destinations), "destinations": destinations[:50]}

@FLIGHTS_INFO_SERVER.tool(title="get_planes_by_code")
async def get_planes_by_code_tool(code: str) -> dict:
    """Get plane information by IATA or ICAO code.

    Args:
        code (str): The IATA code or ICAO code of the plane.

    Returns:
        dict: The plane information or an error message.
    """
    planes = find_planes_by_code(code)
    return {"planes": planes} if planes else {"error": f"No planes found for code {code}"}

@FLIGHTS_INFO_SERVER.tool(title="get_country_codes")
async def get_country_codes_tool(country_name: str) -> dict:
    """Get country codes by country name.

    Args:
        country_name (str): The name of the country to search for.

    Returns:
        dict: The country information or an error message.
    """
    country = find_country_by_name(country_name)
    return {"country": country} if country else {"error": f"Country not found: {country_name}"}

@FLIGHTS_INFO_SERVER.tool(title="find_route_hops")
async def find_route_hops_tool(source_iata: str, destination_iata: str, max_hops: int = 2) -> dict:
    """Find possible flight routes between two airports within a maximum number of hops.
    
    Args:
        source_iata (str): The IATA code of the source airport.
        destination_iata (str): The IATA code of the destination airport.
        max_hops (int): The maximum number of hops allowed.
        
    Returns:
        dict: A list of possible routes found.
    """
    paths = find_route_paths(source_iata, destination_iata, max_hops)
    return {"source": source_iata.upper(), "destination": destination_iata.upper(), "max_hops": max_hops, "paths_found": len(paths), "paths": paths[:25]}

async def main():
    await FLIGHTS_INFO_SERVER.run_async(transport="http", host="0.0.0.0", port=8001, path="/flights_info_server", log_level="debug")

if __name__ == "__main__":
    asyncio.run(main())