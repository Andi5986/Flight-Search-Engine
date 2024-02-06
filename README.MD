# Flight Search Engine

The Flight Search Engine is a Python-based tool designed to help users search for flights by leveraging the Google Flights search via the SERPAPI. It provides an interactive interface to select departure and arrival cities, flight dates, and displays a list of available flight options with detailed information.

## Features

- Load environmental variables for API access.
- Load cities and corresponding airports from a JSON file.
- Select departure and arrival cities through a user interface.
- Select outbound and return flight dates.
- Search for flights using Google Flights via SERPAPI.
- Display search results with detailed flight information, including carbon emissions and layovers.

## Setup

### Requirements

- Python 3.x
- Streamlit
- dotenv Python package
- SERPAPI Python SDK
- A `.env` file with your SERPAPI API key (`SERPAPI_API_KEY`).

### Installation

1. Clone this repository to your local machine.
2. Install the required Python packages:

```bash
pip install streamlit python-dotenv serpapi
```

Create a .env file in the root directory of the project and add your SERPAPI API key:
```bash
SERPAPI_API_KEY=your_api_key_here
```

Place the cities_airports.json file in the root directory of your project. The file should contain a JSON object mapping cities to their corresponding airports.

### Usage
To use the Flight Search Engine, run the Streamlit application from the terminal:

```bash
streamlit run app.py
```

Follow the interactive prompts on the web interface to select your departure and arrival cities, flight dates, and search for flights. The application will display a list of available flights along with detailed information for each flight option.

Contributing
Contributions to the Flight Search Engine are welcome. Please feel free to fork the repository, make changes, and submit pull requests with your improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.# Flight-Search-Engine
