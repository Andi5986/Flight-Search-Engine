from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access the API key
api_key = os.getenv('SERPAPI_API_KEY')

# Use the API key in your parameters
params = {
    "engine": "google_flights",
    "departure_id": "PEK",
    "arrival_id": "AUS",
    "outbound_date": "2024-02-07",
    "return_date": "2024-02-13",
    "currency": "USD",
    "hl": "en",
    "api_key": api_key  # Use the loaded API key
}
search = GoogleSearch(params)

# Perform the search and get results as a dictionary
results = search.get_dict()

# Now, you can process the 'results' dictionary as needed. For example:
best_flights = results.get('best_flights', [])
for flight in best_flights:
    flights = flight.get('flights', [])
    for leg in flights:
        departure_airport = leg['departure_airport']['name']
        arrival_airport = leg['arrival_airport']['name']
        duration = leg['duration']
        airline = leg['airline']
        flight_number = leg['flight_number']
        print(f"Flight {flight_number} by {airline} from {departure_airport} to {arrival_airport}, Duration: {duration} mins")
