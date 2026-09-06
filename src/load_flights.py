import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def connect_to_mysql():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


def load_flights(flights):

    if not flights:
        print("No flights to load.")
        return

    connection = connect_to_mysql()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO raw_flights (
            flight_date,
            airline_code,
            flight_number,
            origin,
            destination,
            scheduled_departure,
            actual_departure,
            scheduled_arrival,
            actual_arrival,
            status,
            delay_minutes
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            airline_code = VALUES(airline_code),
            origin = VALUES(origin),
            destination = VALUES(destination),
            scheduled_departure = VALUES(scheduled_departure),
            actual_departure = VALUES(actual_departure),
            scheduled_arrival = VALUES(scheduled_arrival),
            actual_arrival = VALUES(actual_arrival),
            status = VALUES(status),
            delay_minutes = VALUES(delay_minutes)
    """

    cursor.executemany(insert_query, flights)

    connection.commit()

    print(f"{cursor.rowcount} database operations completed.")

    cursor.close()
    connection.close()