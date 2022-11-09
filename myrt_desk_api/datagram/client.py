"""Datagram client"""

from asyncio import (
    Queue,
    QueueFull
)
from warnings import warn

class DatagramClient:
    """High-level interface for UDP client"""

    def __init__(self, queue_size=0):
        self._queue = Queue(queue_size)
        self._closed = False
        self._transport = None
        self._write_ready_future = None

    def feed_datagram(self, data: bytes, addr: str):
        """Add data to response"""
        try:
            self._queue.put_nowait((data, addr))
        except QueueFull:
            warn('Endpoint queue is full')

    def close(self):
        """Closes datagram"""
        # Manage flag
        if self._closed:
            return
        self._closed = True
        # Wake up
        if self._queue.empty():
            self.feed_datagram(None, None)
        # Close transport
        if self._transport:
            self._transport.close()

    def send(self, data: bytes, addr = None):
        """Send a datagram to the given address."""
        if self._closed:
            raise IOError("Enpoint is closed")
        self._transport.sendto(data, addr)

    async def receive(self):
        """Wait for an incoming datagram and return it with
        the corresponding address.
        This method is a coroutine.
        """
        if self._queue.empty() and self._closed:
            raise IOError("Enpoint is closed")
        data, addr = await self._queue.get()
        if data is None:
            raise IOError("Enpoint is closed")
        return data, addr

    def abort(self):
        """Close the transport immediately."""
        if self._closed:
            raise IOError("Enpoint is closed")
        self._transport.abort()
        self.close()

    async def drain(self):
        """Drain the transport buffer below the low-water mark."""
        if self._write_ready_future is not None:
            await self._write_ready_future

    @property
    def address(self):
        """The endpoint address as a (host, port) tuple."""
        return self._transport.get_extra_info("socket").getsockname()

    @property
    def closed(self):
        """Indicates whether the endpoint is closed or not."""
        return self._closed
