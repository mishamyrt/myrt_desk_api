"""MyrtDesk domain"""
from abc import ABC
from asyncio import AbstractEventLoop, Queue

from .transport import SocketMessage, SocketStream


class UnknownCommandError(Exception):
    "Raised when domain receives unknown command"
    pass


class DeskDomain(ABC):
    """MyrtDesk domain base class"""
    code: int = 0

    _stream: SocketStream
    _loop: AbstractEventLoop
    _messages: Queue[SocketMessage]

    def __init__(self, stream: SocketStream, loop: AbstractEventLoop):
        self._stream = stream
        self._loop = loop
        self._messages = Queue(loop=loop)

    async def send(self, command, *args: int) -> bool:
        """Sends command to MyrtDesk"""
        command = [self.code, command.value]
        if len(args) > 0:
            command.extend([*args])
        return await self._stream.send(command)

    async def put_message(self, message: SocketMessage):
        await self._messages.put(message)

    async def next_message(self) -> SocketMessage:
        return await self._messages.get()
