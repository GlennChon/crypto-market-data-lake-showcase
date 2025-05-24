import os
import psycopg2
import polars as pl
from typing import Optional, Sequence


class Database:
    def __init__(
        self,
        host: str = os.environ["CRYPTO_DB_HOST"],
        port: int = int(os.environ["CRYPTO_DB_PORT"]),
        dbname: str = os.environ["CRYPTO_DB_NAME"],
        user: str = os.environ["CRYPTO_DB_USER"],
        password: str = os.environ["CRYPTO_DB_PASS"],
    ):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
        }

    def execute(
        self,
        sql: str,
        fetch: bool = False,
        params: Optional[tuple] = None,
        many: Optional[Sequence[tuple]] = None
    ) -> Optional[pl.DataFrame]:
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                if many is not None:
                    cur.executemany(sql, many)
                else:
                    cur.execute(sql, params)

                if fetch:
                    rows = cur.fetchall()
                    columns = [desc[0] for desc in cur.description]
                    return pl.DataFrame(rows, schema=columns)
                else:
                    conn.commit()
                    return None
