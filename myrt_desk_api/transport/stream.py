"""MyrtDesk API stream transport"""
from __future__ import annotations

from asyncio import sleep
from typing import Callable, List, Tuple
from warnings import warn

import asyncio_dgram

from .bytes import high_byte, low_byte
from .constants import API_PORT
from .ping import ping


class Stream():
    """High-level UDP transport for MyrtDesk"""
    _host: str
    _stream: asyncio_dgram.DatagramClient | None

    def __init__(self, host: str):
        self._host = host
        self._stream = None

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

    async def connected(self) -> None:
        """Waiting to connect to a desk."""
        if self._stream is None:
            self._stream = await asyncio_dgram.connect((self._host, API_PORT))

    async def listen(self, handler: Callable) -> None:
        """Listens for incoming messages"""
        while True:
            (message, _) = await self._stream.recv()
            lines = message.decode().split('\n')
            for line in lines:
                handler(line)

    async def send_command(self, request: List[int]) -> None:
        """Sends command to MyrtDesk"""
        await self.connected()
        request_body = []
        length = len(request)
        if length >= 255:
            request_body.append(111) # Long length indicator
            request_body.append(high_byte(length))
            request_body.append(low_byte(length))
        else:
            request_body.append(length)
        request_body.extend(request)
        await self._stream.send(
            bytes(request_body)
        )

    async def send_request(self, request: List[int]) -> Tuple[List[int], bool]:
        """Sends request to MyrtDesk"""
        await self.send_command(request)
        (response_bytes, _) = await self._stream.recv()
        response = list(response_bytes)
        success = True
        if len(response) != response[0] + 1:
            warn(f'Wrong response: {response}')
            success = False
        elif len(response) == 4 and response[3] != 0:
            warn(f'Error received: {response}')
            warn(f'Request: {request}')
            success = False
        return (response, success)
