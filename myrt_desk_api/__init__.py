"""MyrtDesk controller"""
from asyncio import AbstractEventLoop, Event, Task, exceptions, get_event_loop, sleep
from typing import Optional

from async_timeout import timeout

from .backlight import MyrtDeskBacklight
from .domain import DeskDomain
from .legs import MyrtDeskLegs
from .system import MyrtDeskSystem
from .transport import API_PORT, SocketStream

__version__ = "1.0.0"

class MyrtDesk:
    """MyrtDesk controller entity"""
    _stream: SocketStream
    _backlight: MyrtDeskBacklight
    _system: MyrtDeskSystem
    _legs: MyrtDeskLegs
    _domains: list[DeskDomain]
    _loop: AbstractEventLoop
    _listener_task: Optional[Task] = None
    _closed = Event()

    def __init__(self, host="MyrtDesk.local", loop=get_event_loop()):
        stream = SocketStream((host, API_PORT), loop)
        self._loop = loop
        self._stream = stream
        self._backlight = MyrtDeskBacklight(stream, loop)
        self._legs = MyrtDeskLegs(stream, loop)
        self._system = MyrtDeskSystem(stream, loop)
        self._domains = [
            self._backlight,
            self._legs,
            self._system
        ]

    async def connect(self):
        if self._listener_task is not None:
            return
        await self._stream.connect()
        self._listener_task = self._loop.create_task(self._listen_messages())

    async def close(self):
        if self._listener_task is None:
            return
        self._closed.set()
        self._listener_task.cancel()
        await self._stream.close()

    @property
    def backlight(self) -> MyrtDeskBacklight:
        """MyrtDesk backlight controller"""
        return self._backlight

    @property
    def system(self) -> MyrtDeskSystem:
        """MyrtDesk system controller"""
        return self._system

    @property
    def legs(self) -> MyrtDeskLegs:
        """MyrtDesk legs controller"""
        return self._legs

    async def _handle_domain_message(self):
        message = await self._stream.next_message()
        for domain in self._domains:
            if domain.code == message["domain"]:
                await domain.put_message(message)
                return

    async def _listen_messages(self):
        while not self._closed.is_set():
            try:
                async with timeout(2):
                    await self._handle_domain_message()
            except exceptions.TimeoutError:
                pass
