"""MyrtDesk API transport"""

from typing import Union
from warnings import warn
from .datagram import open_endpoint, Endpoint
from .constants import API_PORT
from .bytes import high_byte, low_byte

class MyrtDeskTransport():
    """High-level direct transport for MyrtDesk"""
    _host: str = ''
    _endpoint: Union[Endpoint, type(None)] = None

    def __init__(self, host: str):
        self._host = host

    @property
    def host(self) -> str:
        """Indicates whether the transport is connected."""
        return self._host

    @property
    def connected(self):
        """Indicates whether the transport is connected."""
        return not (self._endpoint is None or self._endpoint.closed)

    async def send_request(self, request: list) -> (list, bool):
        """Sends request to MyrtDesk"""
        if not self.connected:
            await self._connect()
        request_body = []
        length = len(request)
        if length >= 255:
            request_body.append(111)
            request_body.append(high_byte(length))
            request_body.append(low_byte(length))
        else:
            request_body.append(length)
        request_body.extend(request)
        self._endpoint.send(
            bytes(request_body)
        )
        response = list(await self._endpoint.receive())
        success = True
        if len(response) != response[0] + 1:
            warn(f'Wrong response: {response}')
            success = False
        elif len(response) == 4 and response[3] != 0:
            warn(f'Error recieved: {response}')
            warn(f'Request: {request_body}')
            success = False
        return (response, success)

    async def _connect(self):
        self._endpoint = await open_endpoint(
            self._host,
            API_PORT
        )
