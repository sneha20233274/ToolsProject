from db import get_connection
import json

def save_trip(city, start_date, duration_days, prompt, itinerary_data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO trip_plans (city, start_date, duration_days, prompt, generated_itinerary)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """

    cursor.execute(query, (
        city,
        start_date,
        duration_days,
        prompt,
        json.dumps(itinerary_data)
    ))

    trip_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return trip_id
