"""MyrtDesk legs"""

from typing import List, Tuple, Union
from ..domain import MyrtDeskDomain
from ..bytes import low_byte, high_byte
from .constants import (
    DOMAIN_LEGS,
    COMMAND_READ_HEIGHT,
    COMMAND_SET_HEIGHT,
    COMMAND_GET_SENSOR_LENGTH,
    COMMAND_CALIBRATE
)

RGBColor = Tuple[int, int, int]

class MyrtDeskLegs(MyrtDeskDomain):
    """MyrtDesk legs controller constructor"""

    _domain_code = DOMAIN_LEGS

    async def get_height(self) -> Union[None, int]:
        """Get current height"""
        (response, success) = await self.send_command([COMMAND_READ_HEIGHT])
        if not success:
            return None
        return (response[3] << 8) + response[4]

    async def set_height(self, value: int) -> bool:
        """Get current height"""
        (_, success) = await self.send_command([
            COMMAND_SET_HEIGHT,
            high_byte(value),
            low_byte(value),
        ])
        return success

    async def get_sensor_data(self) ->  Union[None, int]:
        """Get current raw distance from sensor"""
        (data, success) = await self.send_command([COMMAND_GET_SENSOR_LENGTH])
        if not success:
            return 0
        value = (data[3] << 8) + data[4]
        return value

    async def caibrate(self) -> bool:
        """Starts desk legs calibration"""
        (_, success) = await self.send_command([COMMAND_CALIBRATE])
        return success
