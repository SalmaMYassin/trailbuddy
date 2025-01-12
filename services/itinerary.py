from openai import OpenAI
from services.places import get_places_nearby
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)
# Set your OpenAI API key

def generate_itinerary(destination: str, duration: int, interests: list, budget: float) -> str:
    """
    Generates a basic travel itinerary using OpenAI API.
    """
    prompt = f"""
    Create a {duration}-day travel itinerary for a trip to {destination}.
    The traveler is interested in {', '.join(interests)} and has a budget of ${budget}.
    Provide a day-by-day plan with activities and approximate costs.
    can you return the response as a json object?
    with a description and total cost for each day, 
    and each activity should have activity being done, name of place, cost, details? 
    and add a notes in the end for any notes
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful travel guide."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"} 
        )
    print(completion.choices[0].message.content)
    return json.loads(completion.choices[0].message.content)




def generate_itinerary_with_places(destination: str, lat: float, lon: float, duration: int, radius: int = 1500):
    """
    Generate a travel itinerary with places from Google Places API.
    :param destination: Destination name (for display purposes).
    :param lat: Latitude of the destination.
    :param lon: Longitude of the destination.
    :param duration: Number of days for the trip.
    :param radius: Radius in meters for nearby places (default: 1500m).
    :return: A string itinerary.
    """
    # Fetch nearby places (e.g., tourist attractions)
    attractions = get_places_nearby(location=f"{lat},{lon}", radius=radius, place_type="tourist_attraction")

    # Limit attractions to the duration (1 attraction per day)
    selected_attractions = attractions[:duration]

    # Build a day-by-day itinerary
    itinerary = f"Destination: {destination}\n"
    for day, place in enumerate(selected_attractions, start=1):
        itinerary += (
            f"Day {day}: Visit {place['name']} - {place['vicinity']}\n"
            f"    Rating: {place.get('rating', 'N/A')}\n"
        )

    # Handle cases where there are fewer attractions than days
    if len(selected_attractions) < duration:
        itinerary += "Some days have no specific attractions due to limited data.\n"

    return itinerary.model_dump_json()
