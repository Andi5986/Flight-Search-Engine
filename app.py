import streamlit as st
import json
from serpapi.google_search import GoogleSearch

class FlightSearchEngine:
    def __init__(self):
        """
        Initializes the FlightSearchEngine instance by loading environment variables
        and cities-airports mappings. This setup is essential for the search engine
        to access API keys and understand the relation between cities and their airports.
        """
        self.load_env_variables()
        self.load_cities_airports()

    def load_env_variables(self):
        """
        Loads environmental variables from a .env file, specifically the SERPAPI_API_KEY
        used for flight search requests. This API key is essential for making requests
        to the search API.
        """
        self.api_key = st.secrets["api_key"]

    def load_cities_airports(self):
        """
        Loads a mapping of cities to airports from a JSON file. This mapping is used
        to allow users to select departure and arrival cities and automatically map
        these selections to their corresponding airports.
        """
        with open("cities_airports.json") as file:
            data = json.load(file)
            self.cities_airports = data["cities_airports"]

    def select_cities(self):
        """
        Provides an interface for the user to select departure and arrival cities
        from a list, which are then used to determine the corresponding airports.
        This selection is made through a graphical interface, leveraging selection boxes.
        """
        self.departure_city = st.selectbox("Departure City", options=list(self.cities_airports.keys()), index=0, key='dep_city')
        self.arrival_city = st.selectbox("Arrival City", options=list(self.cities_airports.keys()), index=1, key='arr_city')

        self.departure_airport = self.cities_airports[self.departure_city][0]
        self.arrival_airport = self.cities_airports[self.arrival_city][0]

    def select_dates(self):
        """
        Provides an interface for the user to select outbound and return dates for the flight.
        These dates are essential for querying available flights within the specified timeframe.
        """
        self.outbound_date = st.date_input("Outbound Date").strftime("%Y-%m-%d")
        self.return_date = st.date_input("Return Date").strftime("%Y-%m-%d")

    def search_flights(self):
        """
        Triggers the flight search based on selected cities and dates upon user request.
        Utilizes the SERPAPI for fetching flight options and then processes these options
        to display them to the user.
        """
        if st.button("Search Flights"):
            params = {
                "engine": "google_flights",
                "api_key": self.api_key,
                "departure_id": self.departure_airport,
                "arrival_id": self.arrival_airport,
                "outbound_date": self.outbound_date,
                "return_date": self.return_date,
                "currency": "USD",
                "hl": "en"
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            self.display_results(results)

    def display_results(self, results):
        """
        Displays the search results to the user, showing the best flight options available.
        For each flight option, details such as the airline, flight number, and total price
        are presented, along with an option to expand for more detailed flight information.
        """
        best_flights = results.get('best_flights', [])
        if best_flights:
            for i, flight in enumerate(best_flights, start=1):
                airline = flight["flights"][0].get("airline", "Flight")
                flight_number = flight["flights"][0].get("flight_number", "")
                total_price = flight.get("price", "N/A")
                expander_title = f"Flight Option ${total_price}: {airline} {flight_number}"
                flight_expander = st.expander(expander_title, expanded=False)
                
                with flight_expander:
                    # Display the airline logo as the first item within the expander
                    airline_logo = flight["flights"][0].get("airline_logo", "")
                    if airline_logo:
                        st.image(airline_logo, width=70)
                    
                    # Then display the rest of the flight details
                    self.display_flight_details(flight)
        else:
            st.write("No flights found.")

    @staticmethod
    def display_flight_details(flight):
        """
        Displays detailed information about a specific flight, including total duration,
        carbon emissions, and leg details such as departure and arrival times, flight number,
        and amenities like legroom and class. This method aims to provide users with all the
        necessary details to make an informed flight choice.
        """
        total_duration = flight.get("total_duration", "N/A")

        carbon_emissions = flight.get("carbon_emissions", {}).get("this_flight", "N/A")
        
        st.write(f"Total Duration: {total_duration} minutes")
        st.write(f"Carbon Emissions: {carbon_emissions}g")
        
        for leg in flight["flights"]:
            st.markdown("**Leg Details:**")
            departure_name = leg["departure_airport"]["name"]
            departure_id = leg["departure_airport"]["id"]
            departure_time = leg["departure_airport"]["time"]
            arrival_name = leg["arrival_airport"]["name"]
            arrival_id = leg["arrival_airport"]["id"]
            arrival_time = leg["arrival_airport"]["time"]
            duration = leg.get("duration", "N/A")
            airplane = leg.get("airplane", "N/A")
            airline = leg.get("airline", "N/A")
            flight_number = leg.get("flight_number", "N/A")
            legroom = leg.get("legroom", "N/A")
            travel_class = leg.get("travel_class", "N/A")
            
            # Displaying the additional details
            st.write(f"**Flight Number:** {flight_number}")
            st.write(f"**Airline:** {airline}")
            st.write(f"**Departure:** {departure_name} ({departure_id}), **Time:** {departure_time}")
            st.write(f"**Arrival:** {arrival_name} ({arrival_id}), **Time:** {arrival_time}")
            st.write(f"**Duration:** {duration} minutes")
            st.write(f"**Airplane:** {airplane}")
            st.write(f"**Class:** {travel_class}")
            st.write(f"**Legroom:** {legroom}")
            
            if "extensions" in leg:
                st.write("**Extensions:**")
                for extension in leg["extensions"]:
                    st.write(f"- {extension}")

        if "layovers" in flight:
            st.markdown("**Layovers:**")
            for layover in flight["layovers"]:
                layover_name = layover.get("name", "N/A")
                layover_duration = layover.get("duration", "N/A")
                st.write(f"{layover_name} for {layover_duration} minutes")

def main():
    st.title('Flight Search Engine')
    engine = FlightSearchEngine()
    engine.select_cities()
    engine.select_dates()
    engine.search_flights()

if __name__ == "__main__":
    main()
