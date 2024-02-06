import pytest
from unittest.mock import patch, MagicMock
from app import FlightSearchEngine
import os
import json

# Mocking streamlit's behavior for tests
@pytest.fixture
def mock_st(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("streamlit.st", mock)
    return mock

# Mocking os.getenv to return a specific API key
@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setattr(os, "getenv", lambda x: "test_api_key" if x == "SERPAPI_API_KEY" else None)

# Mocking json.load for loading cities and airports
@pytest.fixture
def mock_json_load(monkeypatch):
    def mock_load(file):
        return {
            "cities_airports": {
                "CityA": ["AirportA"],
                "CityB": ["AirportB"]
            }
        }
    monkeypatch.setattr(json, "load", mock_load)

# Mocking the GoogleSearch class
class MockGoogleSearch:
    def __init__(self, params):
        self.params = params

    def get_dict(self):
        return {
            "best_flights": [
                {
                    "flights": [
                        {
                            "airline_logo": "http://example.com/logo.png",
                            "departure_airport": {
                                "name": "CityA Airport",
                                "id": "AirportA",
                                "time": "08:00",
                            },
                            "arrival_airport": {
                                "name": "CityB Airport",
                                "id": "AirportB",
                                "time": "12:00",
                            },
                            "duration": "240",
                            "airplane": "Boeing 737",
                            "airline": "Test Airline",
                            "flight_number": "TA123",
                            "legroom": "32 inches",
                            "travel_class": "Economy",
                        }
                    ],
                    "price": "200",
                    "total_duration": "240",
                    "carbon_emissions": {"this_flight": "150kg"},
                }
            ]
        }

@pytest.fixture
def mock_google_search(monkeypatch):
    monkeypatch.setattr("serpapi.google_search.GoogleSearch", MockGoogleSearch)

# Test for loading environment variables
def test_load_env_variables(mock_env):
    engine = FlightSearchEngine()
    engine.load_env_variables()

    # Assert
    assert engine.api_key == "test_api_key", "API key should be loaded from environment variables"

# Test for loading cities and airports mapping
def test_load_cities_airports(mock_json_load):
    engine = FlightSearchEngine()
    engine.load_cities_airports()

    # Assert
    assert engine.cities_airports == {"CityA": ["AirportA"], "CityB": ["AirportB"]}, "Cities and airports should be loaded correctly"

# Parametrized test for search flights
@pytest.mark.parametrize("departure_city,arrival_city,outbound_date,return_date,expected_params", [
    ("CityA", "CityB", "2023-01-01", "2023-01-10", {
        "engine": "google_flights",
        "api_key": "test_api_key",
        "departure_id": "AirportA",
        "arrival_id": "AirportB",
        "outbound_date": "2023-01-01",
        "return_date": "2023-01-10",
        "currency": "USD",
        "hl": "en"
    }),
    # Add more test cases as needed
], ids=["happy_path"])
@patch("app.FlightSearchEngine.display_results")
def test_search_flights(mock_display_results, mock_env, mock_json_load, mock_google_search, departure_city, arrival_city, outbound_date, return_date, expected_params):
    engine = FlightSearchEngine()
    engine.api_key = "test_api_key"
    engine.cities_airports = {"CityA": ["AirportA"], "CityB": ["AirportB"]}
    engine.departure_city = departure_city
    engine.arrival_city = arrival_city
    engine.departure_airport = engine.cities_airports[departure_city][0]
    engine.arrival_airport = engine.cities_airports[arrival_city][0]
    engine.outbound_date = outbound_date
    engine.return_date = return_date

    # Act
    engine.search_flights()

    # Assert
    mock_display_results.assert_called_once()
    assert engine.api_key == expected_params["api_key"], "API key should match expected"
    assert mock_display_results.call_args[0][0]["best_flights"][0]["price"] == "200", "Should display results with correct price"

