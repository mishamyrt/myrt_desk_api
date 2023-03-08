"""MyrtDesk domain"""
from abc import ABC
from typing import List

from .transport import Stream


class DeskDomain(ABC):
    """MyrtDesk domain base class"""
    code: int = 0

    _stream: Stream

    def __init__(self, stream: Stream):
        self._stream = stream

    async def send_command(self, payload: list) -> List[int]:
        """Sends raw command to MyrtDesk"""
        resp = await self._stream.send_command([self.code, *payload])
        return resp

    async def send_request(self, payload: list) -> List[int]:
        """Sends command to MyrtDesk"""
        resp = await self._stream.send_request([self.code, *payload])
        return resp
