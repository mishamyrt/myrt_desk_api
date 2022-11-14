"""MyrtDesk legs"""

from asyncio import wait_for, exceptions
from typing import List, Tuple, Union, Callable
from ..ping import host_down, host_up
from ..domain import MyrtDeskDomain
from ..bytes import low_byte, high_byte
from .ota import update_ota
from .constants import (
    DOMAIN_SYSTEM,
    COMMAND_READ,
    COMMAND_REBOOT,
    COMMAND_LOGS
)

RGBColor = Tuple[int, int, int]

class MyrtDeskSystem(MyrtDeskDomain):
    """MyrtDesk legs controller constructor"""

    _domain_code = DOMAIN_SYSTEM

    async def reboot(self) -> None:
        """Get current height"""
        try:
            await wait_for(self.send_command([COMMAND_REBOOT]), 1.0)
        except exceptions.TimeoutError:
            host = self._transport.host
            await wait_for(host_down(host), 2)
            await wait_for(host_up(host), 2)

    async def update_firmware(self, file: bytes, reporter: Callable):
        """Updates controller firmware"""
        def report_progress (val: float) -> None:
            if reporter is not None:
                reporter(val)
        # pylint: disable-next=protected-access
        await update_ota(self._transport._host, 6100, file, report_progress)

    async def read_logs(self, handle_logs: Callable) -> Union[None, int]:
        """Read logs from device while discontinued"""
        await self.send_command_raw([COMMAND_LOGS])
        await self._transport.listen(handle_logs)
        return
