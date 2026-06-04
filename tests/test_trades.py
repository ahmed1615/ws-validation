SYMBOL =  "BTC/USD"


def get_trade_snapshot(ws_client):
    req_id = ws_client.subscribe("trade", SYMBOL, snapshot=True)
    ws_client.wait_for(lambda message: message.get("req_id") == req_id)
    return ws_client.wait_for(lambda message: message.get("channel") == "trade" and message.get("type") == "snapshot")


def test_trade_message(ws_client):
    snapshot = get_trade_snapshot(ws_client)
    trade = snapshot["data"][0]

    assert snapshot["channel"] == "trade"
    assert snapshot["type"] == "snapshot"
    assert snapshot["data"]
    assert trade["symbol"] == SYMBOL
    assert trade["side"]
    assert trade["ord_type"] in {"limit", "market"}
    assert isinstance(trade["trade_id"], int)


def test_trade_price_positive(ws_client):
    trades = get_trade_snapshot(ws_client)["data"]

    assert all(trade["price"] > 0 for trade in trades)


def test_trade_quantity_positive(ws_client):
    trades = get_trade_snapshot(ws_client)["data"]

    assert all(trade["qty"] > 0 for trade in trades)


def test_trade_timestamps_increasing(ws_client):
    trades = get_trade_snapshot(ws_client)["data"]
    timestamps = [trade["timestamp"] for trade in trades]

    assert timestamps == sorted(timestamps)
