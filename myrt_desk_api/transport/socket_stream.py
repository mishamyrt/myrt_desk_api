"""MyrtDesk API stream transport"""
from __future__ import annotations

import asyncio as aio
from datetime import datetime, timedelta
from threading import Event
from typing import Optional, Tuple

from async_timeout import timeout

from .constants import COMMAND_PING
from .persistent_stream import PersistentDatagramStream
from .ping import ping
from .types import Address, Datagram, SocketMessage

PING_DELTA = timedelta(seconds=15)

class SocketStream():
    """High-level UDP stream transport for MyrtDesk"""
    _stream: PersistentDatagramStream
    _listener_task: Optional[aio.Task] = None
    _peer_address: Optional[Address] = None
    _data_messages_queue: aio.Queue[SocketMessage]
    _status_messages_queue: aio.Queue[Datagram]
    _closed = Event()
    _loop: aio.AbstractEventLoop

    def __init__(self, addr: Tuple[str, int], loop=aio.AbstractEventLoop):
        self._stream = PersistentDatagramStream(addr)
        self._data_messages_queue = aio.Queue()
        self._status_messages_queue = aio.Queue()
        self._loop = loop

    @property
    def host(self) -> str:
        """Returns stream host."""
        host, _ = self._stream.addr
        return host

    @property
    def port(self) -> str:
        """Returns stream host."""
        return self._stream.port

    @property
    def closed(self) -> Event:
        """Stream closed event. If the flag is set - the stream is closed"""
        return self._closed

    async def host_down(self, interval = 0.5):
        """Waits for host to be unavailable"""
        while True:
            if not ping(self.host):
                return
            await aio.sleep(interval)

    async def host_up(self, interval = 0.5):
        """Waits for host to be unavailable"""
        while True:
            if ping(self.host):
                return
            await aio.sleep(interval)

    async def host_active(self) -> bool:
        """Waits for host system to be available"""
        await self._stream.send([2, 0, COMMAND_PING])
        resp = await self._stream.read()
        return self._assert_status(resp[1:])

    async def connect(self):
        await self._stream.connect()
        if self._listener_task is None:
            self._listener_task = self._loop.create_task(self._start_listener())

    async def connected(self):
        if not self._stream.connected:
            await self.connect()

    async def close(self):
        if self._listener_task is not None:
            self._closed.set()
            self._listener_task.cancel()
        if self._stream.connected:
            self._stream.close()
            # await aio.sleep(2)

    async def messages(self):
        while not self._closed.is_set():
            message = await self.next_message()
            yield message

    async def next_message(self) -> SocketMessage:
        return await self._data_messages_queue.get()

    async def send_raw(self, command: SocketMessage) -> bool:
        await self.connected()
        request = [len(command), *command]
        return await self._stream.send(request)

    async def send(self, command: SocketMessage) -> bool:
        """Sends command to MyrtDesk"""
        success = await self.send_raw(command)
        if not success:
           return False
        try:
            async with timeout(2):
                status = await self._next_status_message()
                return status
        except (aio.TimeoutError, TimeoutError, aio.exceptions.CancelledError):
            if not self._closed.is_set():
                await self._stream.reconnect()
            return False

    async def _start_listener(self):
        try:
            while not self._closed.is_set():
                now = datetime.now()
                if now - self._stream.last_send_at > PING_DELTA:
                    await self.host_active()
                await self._handle_message()
        except aio.CancelledError:
            pass

    async def _next_status_message(self) -> SocketMessage:
        message = await self._status_messages_queue.get()
        return self._assert_status(message)

    def _assert_status(self, message: Datagram) -> bool:
        return message[2] == 0

    async def _handle_message(self):
        try:
            async with timeout(20):
                await self.connected()
                data = await self._stream.read()
                if data is None and not self._closed.is_set():
                    await self._stream.reconnect()
                    return
                message = data[1:]
                # Assert message length
                if len(data) != data[0] + 1:
                    return
                if len(data) == 4:
                    await self._status_messages_queue.put(message)
                else:
                    await self._data_messages_queue.put({
                        "domain": message[0],
                        "command": message[1],
                        "body": message[2:]
                    })
        except (TimeoutError, aio.TimeoutError, aio.exceptions.TimeoutError):
            if not self._closed.is_set():
                print("reconnecting")
                await self._stream.reconnect()
