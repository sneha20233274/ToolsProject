import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------
# URLs and Keys
# ----------------------
GOOGLE_GEMINI_API_URL = os.getenv("GOOGLE_GEMINI_API_URL", "https://api.google.com/gemini")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

MAPS_API_KEY = os.getenv("MAPS_API_KEY")
MAPS_API_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

EVENTS_API_KEY = os.getenv("EVENTS_API_KEY")
EVENTS_API_URL = "https://serpapi.com/search.json"

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

