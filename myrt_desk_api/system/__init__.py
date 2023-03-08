"""MyrtDesk legs"""

from asyncio import exceptions, wait_for
from typing import Callable, Tuple, Union

from ..domain import DeskDomain
from .constants import COMMAND_FREE_HEAP, COMMAND_LOGS, COMMAND_REBOOT, DOMAIN_SYSTEM
from .ota import update_ota

RGBColor = Tuple[int, int, int]

class MyrtDeskSystem(DeskDomain):
    """MyrtDesk legs controller constructor"""

    code = DOMAIN_SYSTEM

    async def reboot(self) -> None:
        """Get current height"""
        try:
            await wait_for(self.send_request([COMMAND_REBOOT]), 1.0)
        except exceptions.TimeoutError:
            await wait_for(self._stream.host_down(), 2)
            await wait_for(self._stream.host_up(), 2)

    async def update_firmware(self, file: bytes, reporter: Callable):
        """Updates controller firmware"""
        def report_progress (val: float) -> None:
            if reporter is not None:
                reporter(val)
        await update_ota(self._stream.host, 6100, file, report_progress)

    async def read_heap(self) -> Union[int, None]:
        """Read device free heap"""
        (response, success) = await self.send_request([COMMAND_FREE_HEAP])
        if not success:
            return None
        return (response[3] << 8) + response[4]

    async def read_logs(self, handle_logs: Callable) -> Union[None, int]:
        """Read logs from device while discontinued"""
        await self.send_command([COMMAND_LOGS])
        await self._stream.listen(handle_logs)
        return
