import polars as pl
from db.db import Database

def fetch_ohlcv_to_polars(symbol: str = "ETH/USDT", limit: int = 1000) -> pl.DataFrame:
    db = Database()
    sql = """
        SELECT * FROM ohlcv
        WHERE symbol = %s
        ORDER BY timestamp DESC
        LIMIT %s
    """
    result = db.execute(sql, fetch=True, params=(symbol, limit))
    return result if result is not None else pl.DataFrame()
