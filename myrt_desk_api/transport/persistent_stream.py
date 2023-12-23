import logging
from datetime import datetime
from typing import Optional

from asyncio_datagram import DatagramClient, TransportClosed, connect

from .types import Address, Datagram


class PersistentDatagramStream:
    _host_addr: Address
    _peer_addr: Optional[Address] = None
    _stream: Optional[DatagramClient] = None
    _last_send_at = datetime.now()

    def __init__(self, addr: Address):
        self._host_addr = addr

    async def connect(self):
        logging.debug(f"PersistentDatagramStream: connecting to {self._host_addr}")
        if self._stream is None:
            self._stream = await connect(
                self._host_addr,
                local_addr=self._peer_addr,
                reuse_port=True)
            if self._peer_addr is None:
                self._peer_addr = self._stream.sockname
        logging.debug(f"PersistentDatagramStream: connected to {self._host_addr}")

    def close(self):
        logging.debug("PersistentDatagramStream: close")
        if self._stream is None:
            return
        self._stream.close()
        self._stream = None

    async def reconnect(self):
        if self.connected:
            self.close()
        await self.connect()

    @property
    def last_send_at(self):
        return self._last_send_at

    @property
    def port(self):
        _, port = self._peer_addr
        return port

    @property
    def addr(self):
        return self._host_addr

    @property
    def connected(self):
        return self._stream is not None

    async def read(self) -> Optional[Datagram]:
        if self._stream is None:
            return None
        try:
            data, _ = await self._stream.recv()
            logging.debug(f"PersistentDatagramStream: got data ({list(data)})")
            return list(data)
        except (TransportClosed, RuntimeError):
            logging.debug("PersistentDatagramStream: error on read")
            self._stream = None
        return None

    async def send(self, payload: Datagram) -> bool:
        if self._stream is None:
            return False
        try:
            self._last_send_at = datetime.now()
            await self._stream.send(bytes(payload))
            logging.debug(f"PersistentDatagramStream: sended data {list(payload)}")
            return True
        except (TransportClosed, RuntimeError):
            logging.debug("PersistentDatagramStream: error on write")
            self._stream = None
        return False
