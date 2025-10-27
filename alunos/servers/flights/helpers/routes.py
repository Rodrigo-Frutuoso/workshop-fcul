import os
from helpers.loader import load_dataset

HEADERS_ROUTES = ["airline","airline_id","source_airport","source_airport_id","destination_airport","destination_airport_id","codeshare","stops","equipment"]
FILENAME_ROUTES = "routes.dat"

def get_routes() -> list[dict]:
    """
    Load the routes dataset.

    Returns:
        list[dict]: A list of routes with their details.
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", FILENAME_ROUTES)
    return load_dataset(dataset_path, HEADERS_ROUTES)

def destinations_from_airport(source_iata: str) -> list[str]:
    """Get a list of destination IATA codes from a specific source airport.

    Args:
        source_iata (str): The IATA code of the source airport.

    Returns:
        list[str]: A list of destination IATA codes.
    """
    routes = get_routes()
    s = source_iata.upper()
    dest_codes: list[str] = []
    for r in routes:
        if r.get("source_airport", "").upper() == s:
            dest = r.get("destination_airport", "")
            if dest:
                dest_codes.append(dest.upper())
    return sorted(set(dest_codes))

def find_route_paths(source_iata: str, destination_iata: str, max_hops: int = 2) -> list[list[str]]:
    """Find all possible route paths from a source airport to a destination airport.

    Args:
        source_iata (str): The IATA code of the source airport.
        destination_iata (str): The IATA code of the destination airport.
        max_hops (int, optional): The maximum number of hops allowed. Defaults to 2.

    Returns:
        list[list[str]]: A list of all possible route paths.
    """
    routes = get_routes()
    source = source_iata.upper()
    dest = destination_iata.upper()
    adj: dict[str, set[str]] = {}
    for r in routes:
        s = r.get("source_airport", "").upper()
        d = r.get("destination_airport", "").upper()
        if not s or not d:
            continue
        adj.setdefault(s, set()).add(d)
    paths: list[list[str]] = []
    def dfs(current: str, target: str, hops_left: int, visited: list[str]):
        if hops_left < 0:
            return
        if current == target:
            paths.append(visited.copy())
            return
        for nxt in adj.get(current, []):
            if nxt in visited:
                continue
            visited.append(nxt)
            dfs(nxt, target, hops_left - 1, visited)
            visited.pop()
    dfs(source, dest, max_hops, [source])
    return paths