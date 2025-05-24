from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from db.db import Database
import subprocess

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_latest_timestamp(exchange, symbol, interval):
    db = Database()
    sql = """
        SELECT MAX(timestamp) AS latest
        FROM ohlcv
        WHERE exchange = %s AND symbol = %s AND interval = %s
    """
    df = db.execute(sql, fetch=True, params=(exchange, symbol, interval))
    
    # Defensive fallback
    if df is None or df.is_empty() or df[0, "latest"] is None:
        print("No existing timestamp found. Using default.")
        return "2017-01-01T00:00:00Z"

    return df[0, "latest"].isoformat()

def run_fetch(**context):
    dag_conf = context["dag_run"].conf
    exchange = dag_conf.get("exchange", "binance")
    symbol = dag_conf.get("symbol", "ETH/USDT")
    interval = dag_conf.get("interval", "1h")
    limit = int(dag_conf.get("limit", 1000))
    since = get_latest_timestamp(exchange,symbol,interval)

    command = [
        'python', '/opt/airflow/ingestion/fetch_ohlcv.py',
        '--exchange', exchange,
        '--symbol', symbol,
        '--interval', interval,
        '--since', since,
        '--limit', str(limit),
    ]
    subprocess.run(command, check=True)

with DAG(
    dag_id='ohlcv_ingestion',
    default_args=default_args,
    description='Fetch OHLCV data from exchange and store in crypto-db',
    start_date=datetime(2024, 1, 1),
    schedule='@hourly',
    catchup=False,
    tags=['crypto', 'ohlcv', 'ccxt'],
) as dag:

    fetch_ohlcv = PythonOperator(
        task_id='fetch_binance_eth_usdt',
        python_callable=run_fetch,
    )

    fetch_ohlcv
