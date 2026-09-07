-- Aviation Data Engineering
-- Analytics queries for raw_flights


-- =========================================================
-- 1. Total number of flights
-- =========================================================

SELECT
    COUNT(*) AS total_flights
FROM raw_flights;


-- =========================================================
-- 2. Flights by airline
-- =========================================================

SELECT
    airline_code,
    COUNT(*) AS total_flights
FROM raw_flights
GROUP BY airline_code
ORDER BY total_flights DESC;


-- =========================================================
-- 3. Flights by destination
-- =========================================================

SELECT
    destination,
    COUNT(*) AS total_flights
FROM raw_flights
GROUP BY destination
ORDER BY total_flights DESC;


-- =========================================================
-- 4. Average delay by airline
-- =========================================================

SELECT
    airline_code,
    ROUND(AVG(delay_minutes), 2) AS average_delay_minutes
FROM raw_flights
GROUP BY airline_code
ORDER BY average_delay_minutes DESC;


-- =========================================================
-- 5. Delayed vs on-time flights
-- Delay threshold: more than 15 minutes
-- =========================================================

SELECT
    CASE
        WHEN delay_minutes > 15 THEN 'Delayed'
        ELSE 'On Time'
    END AS flight_category,
    COUNT(*) AS total_flights
FROM raw_flights
GROUP BY flight_category
ORDER BY total_flights DESC;


-- =========================================================
-- 6. Flight status distribution
-- =========================================================

SELECT
    status,
    COUNT(*) AS total_flights
FROM raw_flights
GROUP BY status
ORDER BY total_flights DESC;


-- =========================================================
-- 7. Average delay overall
-- =========================================================

SELECT
    ROUND(AVG(delay_minutes), 2) AS average_delay_minutes
FROM raw_flights;


-- =========================================================
-- 8. Most delayed flights
-- =========================================================

SELECT
    flight_date,
    airline_code,
    flight_number,
    origin,
    destination,
    delay_minutes
FROM raw_flights
WHERE delay_minutes > 0
ORDER BY delay_minutes DESC
LIMIT 10;


-- =========================================================
-- 9. Daily flight volume
-- =========================================================

SELECT
    flight_date,
    COUNT(*) AS total_flights
FROM raw_flights
GROUP BY flight_date
ORDER BY flight_date;


-- =========================================================
-- 10. Airline performance summary
-- =========================================================

SELECT
    airline_code,
    COUNT(*) AS total_flights,
    ROUND(AVG(delay_minutes), 2) AS average_delay_minutes,
    SUM(CASE WHEN delay_minutes > 15 THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(
        100 * SUM(CASE WHEN delay_minutes > 15 THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS delayed_percentage
FROM raw_flights
GROUP BY airline_code
ORDER BY delayed_percentage DESC;