SYMBOL = "ALGO/USD"
BADSYMBOL = "HSHH/HG/"

def get_ticker_snapshot(ws_client):
    req_id = ws_client.subscribe("ticker", SYMBOL, snapshot=True)
    ws_client.wait_for(lambda message: message.get("req_id") == req_id)
    return ws_client.wait_for(
        lambda message: message.get("channel") == "ticker" and message.get("type")
    )


def test_ticker_message(ws_client):
    snapshot = get_ticker_snapshot(ws_client)

    assert snapshot["channel"] == "ticker"
    assert snapshot["type"] == "snapshot"


def test_ticker_schema_validation(ws_client):
    snapshot = get_ticker_snapshot(ws_client)
    ticker = snapshot["data"][0]

    assert ticker["symbol"] == SYMBOL
    assert ticker["bid"] is not None
    assert ticker["ask"] is not None
    assert ticker["last"] is not None
    assert ticker["timestamp"]


def test_ticker_bid_and_ask(ws_client):
    ticker = get_ticker_snapshot(ws_client)["data"][0]

    assert ticker["bid"] < ticker["ask"]


def test_ticker_price_positive(ws_client):
    ticker = get_ticker_snapshot(ws_client)["data"][0]
    assert ticker["last"] > 0
