import requests
from mcp.server.fastmcp import FastMCP
from config import EVENTS_API_KEY, EVENTS_API_URL
mcp = FastMCP(name="EventsServer", stateless_http=True)
@mcp.tool(description="A simple events tool")
def get_events(location: str, date_range: str = None) -> dict:
    try:
        print(f"Fetching events for location: {location} with date_range: {date_range}")  # Debug
        query = f"Events in {location}"
        params = {
            "engine": "google_events",
            "q": query,
            "hl": "en",
            "gl": "IN",
            "api_key": EVENTS_API_KEY
        }

        if date_range:
            params["htichips"] = f"date:{date_range}"

        response = requests.get(EVENTS_API_URL, params=params)
        data = response.json()

        print("SerpApi Raw Response:", data)  # Debug

        events_results = data.get("events_results", [])
        event_urls = [event.get("link") for event in events_results]

        return {"success": True, "data": {"events": events_results, "urls": event_urls}}
    except Exception as e:
        return {"success": False, "error": str(e)}