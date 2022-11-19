"""Provide high-level UDP endpoints for asyncio"""
from asyncio import (
    DatagramProtocol,
    DatagramTransport,
    get_event_loop
)
from typing import Tuple
from warnings import warn
from random import randint
from .client import DatagramClient

class Endpoint(DatagramClient):
    """High-level interface for UDP remote enpoints.
    It is initialized with an optional queue size for the incoming datagrams.
    """
    addr: Tuple[str, int] = ("", 0)

    # pylint: disable-next=arguments-differ
    def send(self, data):
        """Send a datagram to the remote host."""
        super().send(data, self.addr)

    async def receive(self):
        """
        Wait for an incoming datagram from the remote host.
        This method is a coroutine.
        """
        data, _ = await super().receive()
        return data

class DatagramEndpointProtocol(DatagramProtocol):
    """Datagram protocol for the endpoint high-level interface."""
    # pylint: disable=protected-access

    def __init__(self, endpoint: Endpoint):
        self._endpoint = endpoint

    def connection_made(self, transport: DatagramTransport):
        self._endpoint._transport = transport

    def connection_lost(self, exc: Exception):
        assert exc is None
        if self._endpoint._write_ready_future is not None:
            self._endpoint._write_ready_future.set_result(None)
        self._endpoint.close()

    def datagram_received(self, data: bytes, addr: str):
        self._endpoint.feed_datagram(data, addr)

    def error_received(self, exc: Exception):
        msg = "Endpoint received an error: {!r}"
        warn(msg.format(exc))

    def pause_writing(self):
        assert self._endpoint._write_ready_future is None
        loop = self._endpoint._transport._loop
        self._endpoint._write_ready_future = loop.create_future()

    def resume_writing(self):
        assert self._endpoint._write_ready_future is not None
        self._endpoint._write_ready_future.set_result(None)
        self._endpoint._write_ready_future = None

async def open_endpoint(host: str, port: str, queue_size=0, **kwargs) -> Endpoint:
    """Open and return a datagram endpoint."""
    loop = get_event_loop()
    endpoint = Endpoint(queue_size)
    endpoint.addr = host, port
    kwargs['local_addr'] = "0.0.0.0", randint(100, 65535)
    kwargs['protocol_factory'] = lambda: DatagramEndpointProtocol(endpoint)
    await loop.create_datagram_endpoint(**kwargs)
    return endpoint
