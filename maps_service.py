import requests
from mcp.server.fastmcp import FastMCP
from config import MAPS_API_KEY, MAPS_API_URL
mcp = FastMCP(name="MapsServer", stateless_http=True)
@mcp.tool(description="A simple routes tool")
def get_route(origin: str, destination: str) -> dict:
    try:
        headers = {
            "Authorization": MAPS_API_KEY
        }
        params = {
            "start": origin,       # must be lon,lat
            "end": destination     # must be lon,lat
        }
        response = requests.get(MAPS_API_URL, headers=headers, params=params)
        data = response.json()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}