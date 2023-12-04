"""MyrtDesk API stream transport"""
from __future__ import annotations

from asyncio import (
    CancelledError,
    Queue,
    Task,
    TimeoutError,
    create_task,
    sleep,
    timeout,
    wait,
)
from datetime import datetime, timedelta
from threading import Event
from typing import List, Optional

import asyncio_dgram
from typing_extensions import TypedDict

from .constants import API_PORT, COMMAND_PING
from .ping import ping

SocketMessageBody = List[int]
SocketMessage = TypedDict('SocketMessage', {
    'domain': int,
    'command': int,
    'body': SocketMessageBody
})

class SocketStream():
    """High-level UDP stream transport for MyrtDesk"""
    _host: str
    _stream: Optional[asyncio_dgram.DatagramClient] = None
    _listener_task: Optional[Task] = None
    _data_messages_queue: Queue[SocketMessage] = Queue()
    _status_messages_queue: Queue[SocketMessageBody] = Queue()
    _closed = Event()

    def __init__(self, host: str):
        self._host = host

    @property
    def host(self) -> str:
        """Returns stream host."""
        return self._host

    async def host_down(self, interval = 0.5):
        """Waits for host to be unavailable"""
        while True:
            if not ping(self._host):
                return
            await sleep(interval)

    async def host_up(self, interval = 0.5):
        """Waits for host to be unavailable"""
        while True:
            if ping(self._host):
                return
            await sleep(interval)

    async def host_active(self) -> bool:
        """Waits for host system to be available"""
        await self.send_request([0, COMMAND_PING])
        resp, _ = await self._stream.recv()
        message = list(resp)[1:]
        return self._assert_status(message)

    async def connect(self):
        await self.connected()
        self._listener_task = create_task(self._start_listener())

    async def close(self):
        self.disconnect()
        if self._listener_task is not None:
            self._closed.set()
            await wait([self._listener_task])

    async def connected(self):
        """Waiting to connect to a desk."""
        if self._stream is None:
            self._stream = await asyncio_dgram.connect((self._host, API_PORT))

    def disconnect(self):
        if self._stream is None:
            return
        self._stream.close()
        self._stream = None

    async def send_request(self, command: SocketMessage) -> None:
        """Sends request to MyrtDesk"""
        await self.connected()
        request_body = [len(command)]
        request_body.extend(command)
        request = bytes(request_body)
        try:
            await self._stream.send(request)
        except:  # noqa: E722
            self.disconnect()

    async def messages(self):
        while not self._closed.is_set():
            message = await self.next_message()
            yield message

    async def next_message(self) -> SocketMessage:
        return await self._data_messages_queue.get()

    async def send(self, request: SocketMessage) -> bool:
        """Sends command to MyrtDesk"""
        self._intercept_status_message = True
        await self.send_request(request)
        status = await self._next_status_message()
        return status

    async def _start_listener(self):
        next_ping = datetime(1996, 4, 27, 5, 30)
        try:
            while not self._closed.is_set():
                now = datetime.now()
                if now > next_ping:
                    if not await self.host_active():
                        self.disconnect()
                        return
                    next_ping = now + timedelta(seconds=20)
                await self._handle_message()
        except CancelledError:
            pass

    async def _next_status_message(self) -> SocketMessage:
        message = await self._status_messages_queue.get()
        return self._assert_status(message)

    def _assert_status(self, message: SocketMessageBody) -> bool:
        return message[2] == 0

    async def _handle_message(self):
        try:
            async with timeout(10):
                await self.connected()
                data, _ = await self._stream.recv()
                response = list(data)
                message = response[1:]
                # Assert message length
                if len(response) != response[0] + 1:
                    return
                if len(response) == 4:
                    await self._status_messages_queue.put(message)
                else:
                    await self._data_messages_queue.put({
                        "domain": message[0],
                        "command": message[1],
                        "body": message[2:]
                    })
        except TimeoutError:
            pass
