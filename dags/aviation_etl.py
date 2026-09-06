from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="aviation_etl",
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False,
    tags=["aviation", "etl", "mysql"],
)
def aviation_etl():

    @task
    def extract():
        from extract_flights import extract_flights

        flights = extract_flights()

        print(f"Flights extracted: {len(flights)}")

        if not flights:
            raise ValueError("No flights were extracted from the API.")

        return flights

    @task
    def transform(flights):
        from transform_flights import transform_flights

        transformed = transform_flights(flights)

        print(f"Flights transformed: {len(transformed)}")

        if not transformed:
            raise ValueError("No flights remained after transformation.")

        return transformed

    @task
    def load(flights):
        from load_flights import load_flights

        load_flights(flights)

        print(f"Flights loaded: {len(flights)}")

    @task
    def validate():
        import os
        import mysql.connector
        from dotenv import load_dotenv

        # Load project environment variables
        load_dotenv("/opt/airflow/.env")

        mysql_host = os.getenv("MYSQL_HOST")
        mysql_user = os.getenv("MYSQL_USER")
        mysql_password = os.getenv("MYSQL_PASSWORD")
        mysql_database = os.getenv("MYSQL_DATABASE")

        if not mysql_host:
            raise ValueError("MYSQL_HOST is not configured.")

        if not mysql_user:
            raise ValueError("MYSQL_USER is not configured.")

        if not mysql_database:
            raise ValueError("MYSQL_DATABASE is not configured.")

        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
        )

        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM raw_flights")

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        print(f"Total flights currently in MySQL: {count}")

        if count == 0:
            raise ValueError("Validation failed: raw_flights is empty.")

        print("Database validation successful.")

    extracted = extract()
    transformed = transform(extracted)
    loaded = load(transformed)
    validated = validate()

    loaded >> validated


aviation_etl()