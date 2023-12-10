"""MyrtDesk system domain"""

from asyncio import exceptions, wait_for
from typing import Callable, Union

from myrt_desk_api.domain import DeskDomain, UnknownCommandError
from myrt_desk_api.transport import from_byte_pair

from .ota import update_ota
from .types import DOMAIN_SYSTEM, Command


class MyrtDeskSystem(DeskDomain):
    """MyrtDesk legs controller constructor"""

    code = DOMAIN_SYSTEM

    async def reboot(self) -> None:
        """Get current height"""
        try:
            await wait_for(self.send(Command.REBOOT), 1.0)
        except exceptions.TimeoutError:
            await wait_for(self._stream.host_down(), 2)
            await wait_for(self._stream.host_up(), 2)

    async def update_firmware(self, file: bytes, reporter: Callable):
        """Updates controller firmware"""
        def report_progress (val: float) -> None:
            if reporter is not None:
                reporter(val)
        await update_ota(self._stream.host, 6100, file, report_progress)

    async def request_heap(self) -> bool:
        """Requests device free heap"""
        return await self.send(Command.READ_FREE_HEAP)

    async def read_heap(self) -> Union[int, None]:
        """Read device free heap"""
        success = await self.request_heap()
        if not success:
            return None
        return await self.next_heap()

    async def next_heap(self) -> int:
        message = await self.next_message()
        if message['command'] == Command.BROADCAST_FREE_HEAP.value:
            [high, low] = message['body']
            return from_byte_pair(high, low)
        else:
            raise UnknownCommandError(f"Command {message['command']} is unknown")
