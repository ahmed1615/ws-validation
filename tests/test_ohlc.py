SYMBOL = "ALGO/USD"
INTERVAL = 5


def get_ohlc_snapshot(ws_client):
    req_id = ws_client.subscribe("ohlc", SYMBOL, snapshot=True, interval=INTERVAL)
    ws_client.wait_for(lambda message: message.get("req_id") == req_id)
    return ws_client.wait_for(lambda message: message.get("channel") == "ohlc" and message.get("type") == "snapshot")


def test_ohlc_message(ws_client):
    snapshot = get_ohlc_snapshot(ws_client)
    candle = snapshot["data"][0]

    assert snapshot["channel"] == "ohlc"
    assert snapshot["type"] == "snapshot"
    assert snapshot["data"]
    assert candle["symbol"] == SYMBOL
    assert candle["interval"] == INTERVAL
    assert candle["interval_begin"]


def test_ohlc_high_vs_open(ws_client):
    candle = get_ohlc_snapshot(ws_client)["data"][0]

    assert candle["high"] >= candle["open"]


def test_ohlc_high_vs_close(ws_client):
    candle = get_ohlc_snapshot(ws_client)["data"][0]

    assert candle["high"] >= candle["close"]


def test_ohlc_low_vs_open_and_close(ws_client):
    candle = get_ohlc_snapshot(ws_client)["data"][0]

    assert candle["low"] <= candle["open"]
    assert candle["low"] <= candle["close"]
