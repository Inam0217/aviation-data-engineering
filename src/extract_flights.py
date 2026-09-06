import os

import requests
from dotenv import load_dotenv

from transform_flights import transform_flights


load_dotenv()


def extract_flights():
    api_key = os.getenv("AVIATION_API_KEY")

    url = "https://api.aviationstack.com/v1/flights"

    params = {
        "access_key": api_key,
        "dep_iata": "ISB",
        "flight_status": "landed",
        "limit": 5
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get("data", [])


if __name__ == "__main__":

    api_flights = extract_flights()

    print("Flights extracted:", len(api_flights))

    transformed_flights = transform_flights(api_flights)

    print("Flights transformed:", len(transformed_flights))

    for flight in transformed_flights:
        print(flight)