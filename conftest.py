import pytest

from utils.websocket_client import KrakenWebSocketClient

@pytest.fixture
def ws_client():
    client = KrakenWebSocketClient()
    client.connect()
    yield client
    client.close()
