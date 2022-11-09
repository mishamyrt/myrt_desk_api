"""Provide high-level UDP broadcast for asyncio"""

from asyncio import (
    DatagramProtocol,
    DatagramTransport,
    get_event_loop,
    wait,
    sleep,
    FIRST_COMPLETED
)
from typing import Tuple, Union, Text
from socket import socket, SOL_SOCKET, SO_BROADCAST
from .client import DatagramClient

Address = Tuple[str, int]

class Broadcast(DatagramClient):
    """High-level UDP broadcaster"""

    def read_queue(self):
        """Reads response queue"""
        values = []
        while not self._queue.empty():
            item = self._queue.get_nowait()
            values.append(item)
        return values

    # pylint: disable-next=arguments-differ
    async def receive(self, timeout=1.0, count=0):
        """
        Wait for an incoming datagram for time (in seconds) and return it.
        This method is a coroutine.
        """
        if self._queue.empty() and self._closed:
            raise IOError("Enpoint is closed")
        exit_conditions = [sleep(timeout)]
        if count != 0:
            exit_conditions.append(self._wait_for_count(count))
        await wait(exit_conditions, return_when=FIRST_COMPLETED)
        if self._closed:
            raise IOError("Enpoint is closed")
        return self.read_queue()

    async def _wait_for_count(self, count: int) -> None:
        while True:
            if self._queue.qsize() == count:
                return
            await sleep(0.15)

class BroadcastProtocol(DatagramProtocol):
    """Datagram broadcast protocol"""
    # pylint: disable=protected-access

    def __init__(self, broadcast: Broadcast):
        self._broadcast = broadcast
        self._transport = None

    def connection_made(self, transport: DatagramTransport):
        self._transport = transport
        sock = transport.get_extra_info("socket")  # type: socket.socket
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._broadcast._transport = transport

    def datagram_received(self, data: Union[bytes, Text], addr: Address):
        self._broadcast.feed_datagram(data, addr)

async def open_broadcast(addr: Address) -> Broadcast:
    """Creates datagram broadcast"""
    loop = get_event_loop()
    broadcast = Broadcast()
    await loop.create_datagram_endpoint(
        remote_addr=addr,
        protocol_factory=lambda: BroadcastProtocol(broadcast),
        allow_broadcast=True
    )
    return broadcast
