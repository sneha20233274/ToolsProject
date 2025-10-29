from fastapi import FastAPI, Request
import httpx
import psycopg2
import os

app = FastAPI()

# ✅ DB CONNECTION
def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "postgres"),
        database=os.environ.get("DB_NAME", "tripdb"),
        user=os.environ.get("DB_USER", "tripuser"),
        password=os.environ.get("DB_PASS", "trippass"),
        port=int(os.environ.get("DB_PORT", 5432))
    )


# ✅ FRONTEND CALLS THIS ENDPOINT
@app.post("/plan_trip")
async def plan_trip(request: Request):
    try:
        data = await request.json()
        city = data["city"]
        start_date = data["start_date"]
        duration = data["duration"]
        user_prompt = data["prompt"]

        final_prompt = f"Plan a {duration}-day trip to {city} starting {start_date} with local events and sightseeing."

        # ✅ Call your MCP-powered AI system (client-like functionality)
        async with httpx.AsyncClient() as http:
            ai_response = await http.post(
                "https://toolsproject.onrender.com/agent",
                json={"prompt": final_prompt}
            )

        itinerary = ai_response.json().get("response", "No itinerary generated")

        # ✅ Save to database
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO trip_plans (city, start_date, duration_days, prompt, generated_itinerary)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (city, start_date, duration, user_prompt, itinerary),
        )
        trip_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {
            "status": "success",
            "trip_id": trip_id,
            "itinerary": itinerary
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}


@app.get("/")
def root():
    return {"message": "Trip Planner API is running 🚀"}
if __name__ == "__main__":
    print("Server running…")


