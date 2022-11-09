"""MyrtDesk legs"""

from typing import List, Tuple, Union, Callable
from ..domain import MyrtDeskDomain
from ..bytes import low_byte, high_byte
from .ota import update_ota
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
        await self.send_command([COMMAND_REBOOT])
        return

    async def update_firmware(self, file: bytes, reporter: Callable):
        """Updates controller firmware"""
        def report_progress (val: float) -> None:
            if reporter is not None:
                reporter(val)
        # pylint: disable-next=protected-access
        await update_ota(self._transport._host, 6100, file, report_progress)
