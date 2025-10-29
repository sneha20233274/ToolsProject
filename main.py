import contextlib
from fastapi import FastAPI
from events_service import mcp as events_mcp
from weather_service import mcp as weather_mcp
from maps_service import mcp as maps_mcp
import os


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(maps_mcp.session_manager.run())
        await stack.enter_async_context(events_mcp.session_manager.run())
        await stack.enter_async_context(weather_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/events", events_mcp.streamable_http_app())
app.mount("/weather", weather_mcp.streamable_http_app())
app.mount("/maps", maps_mcp.streamable_http_app())

# @app.post("/save_trip")
# async def save_trip_api(request: Request):
#     data = await request.json()
#     city = data["city"]
#     start_date = data["start_date"]
#     duration = data["duration"]
#     prompt = data["prompt"]
#     itinerary_json = data["itinerary"]

#     trip_id = handle_user_trip(city, start_date, duration, prompt, itinerary_json)
#     return {"status": "success" if trip_id else "failed", "trip_id": trip_id}

PORT = os.environ.get("PORT", 10000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)