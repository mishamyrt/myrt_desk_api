"""MyrtDesk legs domain"""

from typing import Union

from myrt_desk_api.domain import DeskDomain, UnknownCommandError
from myrt_desk_api.transport import from_byte_pair, high_byte, low_byte

from .types import DOMAIN_LEGS, Command


class MyrtDeskLegs(DeskDomain):
    """MyrtDesk legs controller constructor"""

    code = DOMAIN_LEGS

    async def request_height(self) -> Union[None, int]:
        """Get current height"""
        return await self.send(Command.READ_HEIGHT)

    async def read_height(self) -> Union[None, int]:
        """Get current height"""
        success = await self.request_height()
        if not success:
            return None
        return await self.next_state()

    async def set_height(self, value: int) -> bool:
        """Get current height"""
        return await self.send(
            Command.SET_HEIGHT,
            high_byte(value),
            low_byte(value),
        )

    async def next_state(self) -> int:
        message = await self.next_message()
        if message['command'] == Command.BROADCAST_STATE.value:
            [high, low] = message['body']
            return from_byte_pair(high, low)
        else:
            print(message)
            raise UnknownCommandError()

    async def calibrate(self) -> bool:
        """Starts desk legs calibration"""
        return await self.send(Command.CALIBRATE)
