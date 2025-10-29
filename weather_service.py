import requests
from mcp.server.fastmcp import FastMCP
from config import WEATHER_API_KEY, WEATHER_API_URL

mcp = FastMCP(name="WeatherServer", stateless_http=True)

@mcp.tool(description="A simple weather tool")
def get_weather(location: str, date: str) -> dict:
    try:
        response = requests.get(
            WEATHER_API_URL,
            params={"q": location, "date": date, "appid": WEATHER_API_KEY}
        )
        data = response.json()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
   





