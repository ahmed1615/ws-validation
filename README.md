# Kraken WebSocket Tests

Lightweight regression tests for Kraken's public WebSocket v2 market-data channels.

## Scope

- Python 3.12
- pytest
- websocket-client
- Public channels: book, ticker, trade, ohlc
- Negative auth check for Orders/Level3 (no token)
- No Kraken account required

## What this suite checks

- Subscription acknowledgements
- Market-data messages arrive for each channel
- Basic market-data structure and ordering rules
- Simple regression coverage for price, quantity, and candle relationships
- Level3 unauthenticated request rejection behavior

## Setup

Create a virtual environment and install dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run tests

```bash
pytest
```

Run specific files:

```bash
pytest tests/test_book.py -q
pytest tests/test_ticker.py -q
pytest tests/test_trades.py -q
pytest tests/test_ohlc.py -q
pytest tests/test_orders.py -q
```

Required `.env` config (unless you pass URL explicitly in code):

```bash
KRAKEN_WS_URL=wss://ws.kraken.com/v2
```

Example `.env` file location:

```bash
/Kraken-challange/.env
```

## Docker

```bash
docker build -t kraken-websocket-tests .
docker run --rm kraken-websocket-tests
```

If you see `docker build requires exactly 1 argument`, make sure the final `.` is present. It is the build context.

## Test Files

- `tests/test_book.py`: Book snapshot/ordering assertions
- `tests/test_ticker.py`: Ticker schema, prices, and bad-symbol negative case
- `tests/test_trades.py`: Trades schema, positive price/qty, timestamp ordering
- `tests/test_ohlc.py`: Candle relationships (`high/open/close`, `low/open/close`)
- `tests/test_orders.py`: Orders/Level3 unauthenticated rejection assertion

## Notes

- Mix of `BTC/USD` and `ALGO/USD` is used across channels for practical live-feed coverage.
- The suite intentionally stays small and direct instead of introducing a framework or extra abstraction.
- Live WebSocket tests can still be affected by network issues or temporary API instability.
