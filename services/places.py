import googlemaps  
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('GOOGLE_CLOUD_API_KEY')

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=api_key)


def get_lat_lon_from_place(place_name: str):
    """
    Get latitude and longitude for a given place name.
    :param place_name: The name of the place (e.g., "Paris").
    :return: A tuple with latitude and longitude, or None if not found.
    """
    try:
        geocode_result = gmaps.geocode(place_name)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
    
def get_places_nearby(location: str, radius: int, place_type: str):
    """
    Fetch nearby places based on location, radius, and type.
    :param location: Location in "latitude,longitude" format (e.g., "48.8566,2.3522" for Paris).
    :param radius: Search radius in meters (e.g., 1000 for 1 km).
    :param place_type: Type of place (e.g., 'restaurant', 'tourist_attraction').
    :return: List of nearby places.
    """
    try:
        places = gmaps.places_nearby(
            location=get_lat_lon_from_place(location),
            radius=radius,
            type=place_type
        )
        return places.get("results", [])
    except Exception as e:
        return {"error": str(e)}
