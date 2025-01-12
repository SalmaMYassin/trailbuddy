from fastapi import FastAPI
from models.user_preferences import UserPreferences
from services.itinerary import generate_itinerary
from services.places import get_places_nearby

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personalized Travel App!"}


@app.post("/preferences/")
def collect_preferences(preferences: UserPreferences):
    return {"message": "Preferences received!", "data": preferences}

@app.post("/generate-itinerary/")
def create_itinerary(preferences: UserPreferences):
    itinerary = generate_itinerary(
        destination=preferences.destination,
        duration=preferences.duration,
        interests=preferences.interests,
        budget=preferences.budget
    )
    return {"destination": preferences.destination, "itinerary": itinerary}


@app.get("/places/")
def fetch_places(location: str, radius: int = 1000, place_type: str = "tourist_attraction"):
    """
    Fetch nearby places based on location, radius, and type.
    :param location: Location in "latitude,longitude" format (e.g., "48.8566,2.3522").
    :param radius: Search radius in meters (default: 1000).
    :param place_type: Type of place (e.g., 'restaurant', 'tourist_attraction').
    :return: List of places.
    """
    places = get_places_nearby(location, radius, place_type)
    return {"places": places}
