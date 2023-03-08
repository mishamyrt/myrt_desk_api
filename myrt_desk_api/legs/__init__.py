"""MyrtDesk legs"""

from typing import Tuple, Union

from myrt_desk_api.domain import DeskDomain
from myrt_desk_api.transport import from_byte_pair, high_byte, low_byte

from .constants import (
    COMMAND_CALIBRATE,
    COMMAND_GET_SENSOR_LENGTH,
    COMMAND_READ_HEIGHT,
    COMMAND_SET_HEIGHT,
    DOMAIN_LEGS,
)


class MyrtDeskLegs(DeskDomain):
    """MyrtDesk legs controller constructor"""

    code = DOMAIN_LEGS

    async def get_height(self) -> Union[None, int]:
        """Get current height"""
        (response, success) = await self.send_request([COMMAND_READ_HEIGHT])
        if not success:
            return None
        return from_byte_pair(response[3], response[4])

    async def set_height(self, value: int) -> bool:
        """Get current height"""
        (_, success) = await self.send_request([
            COMMAND_SET_HEIGHT,
            high_byte(value),
            low_byte(value),
        ])
        return success

    async def get_sensor_data(self) ->  Union[None, int]:
        """Get current raw distance from sensor"""
        (data, success) = await self.send_request([COMMAND_GET_SENSOR_LENGTH])
        if not success:
            return 0
        return from_byte_pair(data[3], data[4])

    async def calibrate(self) -> bool:
        """Starts desk legs calibration"""
        (_, success) = await self.send_request([COMMAND_CALIBRATE])
        return success
