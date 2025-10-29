from trip_repository import save_trip

def handle_user_trip(city, start_date, duration_days, prompt, itinerary_json):
    try:
        trip_id = save_trip(city, start_date, duration_days, prompt, itinerary_json)
        print(f"✅ Trip saved in DB with ID: {trip_id}")
        return trip_id
    except Exception as e:
        print(f"❌ DB save failed: {e}")
        return None
