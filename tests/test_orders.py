SYMBOL = "ALGO/USD"


def test_orders_auth_error(ws_client):
    ws_client.subscribe("level3", SYMBOL, snapshot=True)

    response = ws_client.wait_for(
        lambda message: message.get("method") == "subscribe" and message.get("success") is False,
        timeout=10,
    )

    assert response["method"] == "subscribe"
    assert response["success"] is False
    assert "Private data and trading are unavailable on this endpoint" in response["error"]
    assert "ws-auth.kraken.com" in response["error"]
