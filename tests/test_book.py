from datetime import datetime


SYMBOL = "BTC/USD"


def get_book_snapshot(ws_client):
    req_id = ws_client.subscribe("book", SYMBOL, snapshot=True, depth=10)
    ws_client.wait_for(lambda message: message.get("req_id") == req_id)
    return ws_client.wait_for(lambda message: message.get("channel") == "book" and message.get("type") == "snapshot")


def test_book_schema_validation(ws_client):
    req_id = ws_client.subscribe("book", SYMBOL, snapshot=True, depth=10)

    acknowledgement = ws_client.wait_for(lambda message: message.get("req_id") == req_id)

    assert acknowledgement["method"] == "subscribe"
    assert acknowledgement["success"] is True
    assert acknowledgement["result"]["channel"] == "book"


def test_book_message(ws_client):
    snapshot = get_book_snapshot(ws_client)
    book = snapshot["data"][0]

    assert snapshot["channel"] == "book"
    assert snapshot["type"] == "snapshot"
    assert book["symbol"] == SYMBOL
    assert isinstance(book["checksum"], int)
    assert isinstance(book["timestamp"], str)
    datetime.fromisoformat(book["timestamp"].replace("Z", "+00:00"))

def test_book_bid_and_ask(ws_client):
    snapshot = get_book_snapshot(ws_client)
    book = snapshot["data"][0]

    best_bid = max(level["price"] for level in book["bids"])
    best_ask = min(level["price"] for level in book["asks"])

    assert best_bid < best_ask


def test_book_bids_sorting(ws_client):
    snapshot = get_book_snapshot(ws_client)
    bid_prices = [level["price"] for level in snapshot["data"][0]["bids"]]
    assert bid_prices == sorted(bid_prices, reverse=True)


def test_book_asks_sorting(ws_client):
    snapshot = get_book_snapshot(ws_client)
    ask_prices = [level["price"] for level in snapshot["data"][0]["asks"]]
    assert ask_prices == sorted(ask_prices)
