from extract_flights import extract_flights
from transform_flights import transform_flights
from load_flights import load_flights


def run_pipeline():

    print("Starting aviation ETL pipeline...")

    # EXTRACT
    api_flights = extract_flights()
    print(f"Flights extracted: {len(api_flights)}")

    # TRANSFORM
    transformed_flights = transform_flights(api_flights)
    print(f"Flights transformed: {len(transformed_flights)}")

    # LOAD
    load_flights(transformed_flights)

    print("Aviation ETL pipeline completed!")


if __name__ == "__main__":
    run_pipeline()