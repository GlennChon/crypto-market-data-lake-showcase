CREATE TABLE IF NOT EXISTS ohlcv (
    id SERIAL PRIMARY KEY,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL, -- e.g., '1m', '1h', '1d'
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    UNIQUE(exchange, symbol, interval, timestamp)
);

-- Optional indexes to improve query performance
CREATE INDEX IF NOT EXISTS idx_ohlcv_exchange_symbol_time
ON ohlcv (exchange, symbol, interval, timestamp DESC);
