"""MyrtDesk domain"""
from typing import List
from .transport import MyrtDeskTransport


class MyrtDeskDomain:
    """MyrtDesk domain prototype"""
    _transport: MyrtDeskTransport = None
    _domain_code = 0

    def __init__(self, transport: MyrtDeskTransport):
        self._transport = transport

    async def _send_command(self, payload: list) -> List[int]:
        resp = await self._transport.send_request([self._domain_code, *payload])
        return resp
