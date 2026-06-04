import json
import os
import time
from contextlib import suppress

import websocket


class KrakenWebSocketClient:
    def __init__(self, url=None, timeout=15):
        env_url = self._read_env_url()
        self.url = url or os.getenv("KRAKEN_WS_URL") or env_url
        if not self.url:
            raise ValueError("WebSocket URL is required. Set KRAKEN_WS_URL in .env or pass url explicitly.")
        self.timeout = timeout
        self._ws = None
        self._req_id = 0

    @staticmethod
    def _read_env_url(env_file=".env"):
        try:
            with open(env_file, "r", encoding="utf-8") as file:
                for line in file:
                    text = line.strip()
                    if not text or text.startswith("#") or "=" not in text:
                        continue
                    key, value = text.split("=", 1)
                    if key.strip() == "KRAKEN_WS_URL":
                        return value.strip().strip('"').strip("'")
        except FileNotFoundError:
            return None
        return None

    def connect(self):
        if self._ws is None:
            self._ws = websocket.create_connection(self.url, timeout=self.timeout)
            self._ws.settimeout(self.timeout)
        return self

    def close(self):
        if self._ws is not None:
            with suppress(Exception):
                self._ws.close()
            self._ws = None

    def send_json(self, payload):
        self._ws.send(json.dumps(payload))

    def subscribe(self, channel, symbols, **params):
        self._req_id += 1
        symbol_list = [symbols] if isinstance(symbols, str) else list(symbols)
        payload = {"method": "subscribe", "params": {"channel": channel, "symbol": symbol_list}, "req_id": self._req_id}
        payload["params"].update(params)
        self.send_json(payload)
        return self._req_id

    def recv_json(self, timeout=None):
        if timeout is not None:
            self._ws.settimeout(timeout)
        raw = self._ws.recv()
        return json.loads(raw)

    def wait_for(self, predicate, timeout=None):
        deadline = time.monotonic() + (timeout or self.timeout)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Timed out waiting for Kraken WebSocket message")
            message = self.recv_json(timeout=remaining)
            if predicate(message):
                return message
