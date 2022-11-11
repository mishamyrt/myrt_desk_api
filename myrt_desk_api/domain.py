"""MyrtDesk domain"""
from typing import List
from .transport import MyrtDeskTransport


class MyrtDeskDomain:
    """MyrtDesk domain prototype"""
    _transport: MyrtDeskTransport = None
    _domain_code: int = 0

    def __init__(self, transport: MyrtDeskTransport):
        self._transport = transport

    @property
    def domain_code(self) -> int:
        """Current domain code"""
        return self._domain_code

    async def send_command_raw(self, payload: list) -> List[int]:
        """Sends raw command to MyrtDesk"""
        resp = await self._transport.send_command([self._domain_code, *payload])
        return resp

    async def send_command(self, payload: list) -> List[int]:
        """Sends command to MyrtDesk"""
        resp = await self._transport.send_request([self._domain_code, *payload])
        return resp
