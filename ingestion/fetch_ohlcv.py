#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime, timezone
import ccxt
import time
from db.db import Database

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch OHLCV and store in Postgres")
    parser.add_argument('--exchange',   type=str, default=os.getenv('EXCHANGE_ID', 'binance'))
    parser.add_argument('--symbol',     type=str, default=os.getenv('SYMBOL', 'ETH/USDT'))
    parser.add_argument('--interval',   type=str, default=os.getenv('INTERVAL', '1h'))
    parser.add_argument('--since',      type=str, default=os.getenv('SINCE', '2017-01-01T00:00:00Z'))
    parser.add_argument('--limit',      type=int, default=int(os.getenv('LIMIT', '1000')))
    return parser.parse_args()

def fetch_ohlcv(exchange_id, symbol, timeframe, since_ts, limit):
    exc_class = getattr(ccxt, exchange_id)
    exchange = exc_class({'enableRateLimit': True})
    exchange.load_markets()
    raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since_ts, limit=limit)
    records = []
    for ts_ms, o, h, l, c, vol in raw:
        ts = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
        records.append((exchange_id, symbol, timeframe, ts, o, h, l, c, vol))
    return records

def store_ohlcv(records, db: Database):
    sql = """
        INSERT INTO ohlcv
          (exchange, symbol, interval, timestamp, open, high, low, close, volume)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (exchange, symbol, interval, timestamp) DO NOTHING;
    """
    db.execute(sql, fetch=False, params=None, many=records)
    return len(records)

if __name__ == "__main__":
    args = parse_args()
    since_ms = ccxt.Exchange().parse8601(args.since)
    exchange_id = args.exchange
    symbol = args.symbol
    interval = args.interval
    limit = args.limit

    db = Database()

    total_inserted = 0
    while True:
        ohlcv = fetch_ohlcv(exchange_id, symbol, interval, since_ms, limit)
        if not ohlcv:
            print("No more data returned.")
            break

        count = store_ohlcv(ohlcv, db)
        total_inserted += count
        print(f"[{datetime.now(timezone.utc).isoformat()}] Inserted {count} rows.")

        if len(ohlcv) < limit:
            break

        last_ts = ohlcv[-1][3]  # datetime object
        since_ms = int(last_ts.timestamp() * 1000) + 1
        time.sleep(0.5)

    print(f"Finished. Total inserted: {total_inserted} rows for {exchange_id} {symbol} {interval}")