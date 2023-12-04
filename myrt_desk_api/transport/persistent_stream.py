from typing import Optional, Tuple

from datetime import datetime
from asyncio_datagram import DatagramClient, TransportClosed, connect

DatagramPayload = list[int]

class PersistentDatagramStream:
    _host_addr: Tuple[str, int]
    _peer_addr: Optional[Tuple[str, int]] = None
    _stream: Optional[DatagramClient] = None
    _last_send_at = datetime.now()

    def __init__(self, addr: Tuple[str, int]):
        self._host_addr = addr

    async def connect(self):
        print("PersistentDatagramStream: connect", self._host_addr)
        if self._stream is None:
            self._stream = await connect(
                self._host_addr,
                local_addr=self._peer_addr,
                reuse_port=True)
            if self._peer_addr is None:
                self._peer_addr = self._stream.sockname
        print("PersistentDatagramStream: connected", self._host_addr)

    def close(self):
        print("PersistentDatagramStream: close")
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

    async def read(self) -> Optional[DatagramPayload]:
        if self._stream is None:
            return None
        try:
            data, _ = await self._stream.recv()
            print("PersistentDatagramStream: readed", list(data))
            return list(data)
        except (TransportClosed, RuntimeError):
            print("PersistentDatagramStream: closed on read")
            self._stream = None
        return None

    async def send(self, payload: DatagramPayload) -> bool:
        if self._stream is None:
            return False
        try:
            self._last_send_at = datetime.now()
            await self._stream.send(bytes(payload))
            print("PersistentDatagramStream: writed", list(payload))
            return True
        except (TransportClosed, RuntimeError):
            print("PersistentDatagramStream: closed on write")
            self._stream = None
        return False
