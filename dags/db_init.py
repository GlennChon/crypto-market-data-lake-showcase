from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

with DAG(
    dag_id='db_init',
    description='Initializes crypto-db ohlcv schema',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['setup', 'postgres', 'schema'],
) as dag:

    init_ohlcv_table = SQLExecuteQueryOperator(
        task_id='create_ohlcv_table',
        conn_id='crypto_postgres',
        sql='/init/sql/init.sql'
    )

    init_ohlcv_table
