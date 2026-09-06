from datetime import datetime


def parse_datetime(value):
    if value is None:
        return None

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).replace(tzinfo=None)


def transform_flights(api_flights):
    transformed_flights = []

    for flight in api_flights:

        departure = flight.get("departure", {})
        arrival = flight.get("arrival", {})
        airline = flight.get("airline", {})
        flight_info = flight.get("flight", {})

        flight_date = flight.get("flight_date")
        airline_code = airline.get("iata")
        flight_number = flight_info.get("iata")

        origin = departure.get("iata")
        destination = arrival.get("iata")

        scheduled_departure = parse_datetime(
            departure.get("scheduled")
        )

        actual_departure = parse_datetime(
            departure.get("actual")
        )

        scheduled_arrival = parse_datetime(
            arrival.get("scheduled")
        )

        actual_arrival = parse_datetime(
            arrival.get("actual")
        )

        status = flight.get("flight_status", "").upper()

        if (
            not flight_number
            or not airline_code
            or not origin
            or not destination
            or not actual_departure
            or not actual_arrival
        ):
            continue

        delay_minutes = int(
            (actual_departure - scheduled_departure).total_seconds() / 60
        )

        transformed_flight = (
            flight_date,
            airline_code.upper(),
            flight_number.upper(),
            origin.upper(),
            destination.upper(),
            scheduled_departure,
            actual_departure,
            scheduled_arrival,
            actual_arrival,
            status,
            delay_minutes
        )

        transformed_flights.append(transformed_flight)

    return transformed_flights