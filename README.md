# Crypto Market Data Lake

This project is the start of a modular, containerized data pipeline for collecting and managing cryptocurrency market data. It uses Apache Airflow for workflow orchestration and PostgreSQL for structured storage. The pipeline supports backfilling, daily ingestion, and is built for future integration with sentiment data and machine learning models.

## Features

- Daily OHLCV data ingestion from crypto exchanges
- Incremental backfill using the last recorded timestamp
- PostgreSQL-backed storage
- Parametrized DAGs for symbol and exchange
- Polars-based analysis support
- Ready for expansion into news sentiment and correlation modeling

## Tools and Technologies

| Tool | Purpose | Link |
|------|---------|------|
| Apache Airflow | Orchestration and scheduling | https://airflow.apache.org |
| Docker Compose | Containerized environment | https://docs.docker.com/compose/ |
| PostgreSQL | Relational data store | https://www.postgresql.org |
| ccxt | Crypto market data access | https://github.com/ccxt/ccxt |
| Polars | High-performance DataFrame library | https://www.pola.rs |
| psycopg2 | PostgreSQL adapter for Python | https://www.psycopg.org |

## Project Structure

crypto-market-data-lake/
    dags/ # Airflow DAG definitions
    ingestion/ # Market data fetch scripts
    db/ # Database utilities
    config/ # Airflow config files
    docker/airflow/ # Custom Dockerfile for Airflow
    .env # Environment configuration
    docker-compose.yml # Docker orchestration


## .env Configuration

Create a `.env` file in the root directory with the following structure:

```dotenv
# Airflow Configuration
AIRFLOW_UID=1000
AIRFLOW_GID=0
AIRFLOW_USERNAME=admin
AIRFLOW_PASSWORD=admin
AIRFLOW_FIRSTNAME=John
AIRFLOW_LASTNAME=Doe
AIRFLOW_EMAIL=john.doe@example.com
AIRFLOW_VERSION=3.0.0

# Crypto Market Database
CRYPTO_DB_HOST=crypto-db
CRYPTO_DB_PORT=5432
CRYPTO_DB_NAME=crypto_data
CRYPTO_DB_USER=crypto
CRYPTO_DB_PASS=securepass


## Getting Started
1. Build:
```bash
docker compose --build
```
2. Start services:
```bash
docker compose up -d
```

3. Access the Airflow UI at:
http://localhost:8080


Future Plans

    Integration with GDELT for historical news data

    News tagging and sentiment analysis

    Correlation modeling between sentiment and price

    Visualization and dashboard support

    API exposure for serving analytics


## Local Development (Optional)

To work with the code outside of Docker (e.g., for development, testing, or editor integration), you can set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
