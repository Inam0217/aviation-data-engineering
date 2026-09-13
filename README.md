# ✈️ Aviation Data Engineering Pipeline

An end-to-end aviation ETL pipeline that extracts flight data from the **AviationStack REST API**, transforms and validates it with **Python**, and loads it into **MySQL** through an **Apache Airflow**-orchestrated workflow.

The pipeline runs as an **hourly batch process** and includes SQL analytics for flight volume, destinations, airline performance, and delays.

## 🏗️ Architecture

```text
AviationStack API
       │
       ▼
    EXTRACT
       │
       ▼
   TRANSFORM
       │
       ▼
      LOAD
       │
       ▼
     MySQL
       │
       ▼
   VALIDATE
       │
       ▼
 SQL ANALYTICS
```

Airflow orchestrates the workflow:

```text
Extract → Transform → Load → Validate
```

## 🛠️ Tech Stack

- **Python**
- **Apache Airflow 3.3.1**
- **Docker / Docker Compose**
- **MySQL 8**
- **SQL**
- **AviationStack API / REST API**
- **Requests**
- **mysql-connector-python**
- **python-dotenv**
- **Git / GitHub**

## 🔄 ETL Pipeline

### 1. Extract

Flight data is retrieved from the AviationStack API using Python and Requests. The current pipeline retrieves landed flights departing from **Islamabad International Airport (`ISB`)**.

### 2. Transform

The transformation layer:

- Selects relevant flight fields
- Normalizes airline, flight, and airport codes
- Converts API timestamps to Python datetime values
- Calculates departure delay in minutes
- Removes records missing required information
- Standardizes flight status values

Key fields include:

```text
flight_date
airline_code
flight_number
origin
destination
scheduled_departure
actual_departure
scheduled_arrival
actual_arrival
status
delay_minutes
```

### 3. Load

Transformed records are loaded into the MySQL `raw_flights` table. Database credentials are supplied through environment variables rather than hardcoded in the source code.

The load process uses `ON DUPLICATE KEY UPDATE` to update existing records when applicable.

### 4. Validate

After loading, Airflow validates the MySQL configuration and connection and checks that `raw_flights` contains records. The workflow fails when validation does not pass.

## ⏰ Airflow Orchestration

The DAG is named `aviation_etl` and uses the schedule:

```text
0 * * * *
```

This runs the ETL pipeline **once every hour**.

The workflow consists of:

```text
Extract → Transform → Load → Validate
```

## 🐳 Docker Environment

Docker Compose provides the Airflow environment and its PostgreSQL metadata database. DAGs and Python source files are mounted into the Airflow services, while project configuration is supplied through `.env`.

Start the environment with:

```bash
docker compose up -d
```

Check services with:

```bash
docker compose ps
```

## 🗄️ MySQL Data Model

Main table:

```text
raw_flights
```

Important columns:

| Column | Description |
|---|---|
| `id` | Record ID |
| `flight_date` | Flight date |
| `airline_code` | Airline IATA code |
| `flight_number` | Flight IATA number |
| `origin` | Origin airport |
| `destination` | Destination airport |
| `scheduled_departure` | Scheduled departure time |
| `actual_departure` | Actual departure time |
| `scheduled_arrival` | Scheduled arrival time |
| `actual_arrival` | Actual arrival time |
| `status` | Flight status |
| `delay_minutes` | Departure delay in minutes |
| `created_at` | Record creation timestamp |

## 📊 SQL Analytics

`sql/analytics.sql` includes queries for:

- Total flight volume
- Flights by airline
- Flights by destination
- Average delay by airline
- Delayed vs. on-time flights
- Flight status distribution
- Overall average delay
- Most delayed flights
- Daily flight volume
- Airline performance and delayed percentage

Example:

```sql
SELECT
    airline_code,
    COUNT(*) AS total_flights,
    ROUND(AVG(delay_minutes), 2) AS average_delay_minutes
FROM raw_flights
GROUP BY airline_code
ORDER BY average_delay_minutes DESC;
```

## 📂 Project Structure

```text
aviation-data-engineering/
│
├── dags/
│   └── aviation_etl.py
├── sql/
│   └── analytics.sql
├── src/
│   ├── extract_flights.py
│   ├── transform_flights.py
│   ├── load_flights.py
│   └── run_pipeline.py
├── screenshots/
│   ├── airflow-dag-overview.png
│   ├── airflow-dag-runs.png
│   └── mysql-workbench-results.png
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## 📸 Screenshots

### Airflow DAG Overview

![Airflow DAG Overview](screenshots/airflow-dag-overview.png)

### Airflow DAG Runs

![Airflow DAG Runs](screenshots/airflow-dag-runs.png)

### MySQL Workbench

![MySQL Workbench Results](screenshots/mysql-workbench-results.png)

## 🧪 Verification

The pipeline has been tested end-to-end:

```text
Extract       ✅
Transform     ✅
Load          ✅
Validate      ✅
```

Successful executions have been verified through Airflow and MySQL output, including transformed flight records and calculated delays.

## 🔐 Configuration & Security

Create a local `.env` file from `.env.example` and configure your credentials:

```text
MYSQL_HOST=host.docker.internal
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=aviation_db
AVIATION_API_KEY=your_aviationstack_api_key
AIRFLOW_JWT_SECRET=your_generated_jwt_secret
```

Security practices:

- Credentials are stored in `.env`
- `.env` is excluded from Git
- `.env.example` contains placeholders only
- API keys and passwords are not hardcoded in Python source files

## 🚀 Run Locally

### 1. Clone

```bash
git clone https://github.com/Inam0217/aviation-data-engineering.git
cd aviation-data-engineering
```

### 2. Configure environment

Copy `.env.example` to `.env` and add your API and MySQL credentials.

### 3. Start Airflow

```bash
docker compose up -d
```

### 4. Run the DAG

Open Airflow and trigger `aviation_etl` manually or allow its hourly schedule to run.

### 5. Verify MySQL

```sql
SELECT COUNT(*) FROM raw_flights;
```

## 🎯 What This Project Demonstrates

- API data extraction
- Python ETL development
- Data transformation and validation
- MySQL integration
- SQL analytics
- Apache Airflow orchestration and scheduling
- Docker-based development
- Environment-based credential management
- Git version control

## 🔮 Future Improvements

- Add automated data-quality tests
- Add Airflow failure alerts
- Build a simple flight-delay dashboard

## 👨‍💻 Author

**Inam Ul Hassan**

Data Engineering Portfolio Project

## 📜 License

This project is intended for educational and portfolio purposes.
