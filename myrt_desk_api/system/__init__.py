"""MyrtDesk legs"""

from typing import List, Tuple, Union
from ..domain import MyrtDeskDomain
from ..bytes import low_byte, high_byte
from .constants import (
    DOMAIN_SYSTEM,
    COMMAND_READ,
    COMMAND_REBOOT,
)

RGBColor = Tuple[int, int, int]

class MyrtDeskSystem(MyrtDeskDomain):
    """MyrtDesk legs controller constructor"""

    _domain_code = DOMAIN_SYSTEM

    async def reboot(self) -> Union[None, int]:
        """Get current height"""
        await self._send_command([COMMAND_REBOOT])
        return
        # if not success:
        #     return None
        # return (response[3] << 8) + response[4]

#define lowByte(w) ((uint8_t) ((w) & 0xff))
#define highByte(w) ((uint8_t) ((w) >> 8))