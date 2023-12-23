from asyncio import wait_for
from typing import Optional

from myrt_desk_api.domain import DeskDomain, UnknownCommandError
from myrt_desk_api.transport import Byte, high_byte, low_byte

from .firmware import Firmware, FirmwareError
from .types import (
    DOMAIN_BACKLIGHT,
    Command,
    Effect,
    Mode,
    ProgressReporter,
    RGBColor,
    State,
)


class MyrtDeskBacklight(DeskDomain):
    """MyrtDesk backlight controller constructor"""
    code = DOMAIN_BACKLIGHT

    async def request_state(self) -> bool:
        """Request backlight state. State will be broadcasted to all connected clients"""
        return await self.send(Command.READ_STATE)

    async def read_state(self) -> State:
        """Reads backlight state. State will be broadcasted to all connected clients"""
        success = await self.request_state()
        if not success:
            return None
        return await self.next_state()

    async def next_state(self) -> State:
        message = await self.next_message()
        if message['command'] == Command.BROADCAST_STATE.value:
            # pylint: disable-next=invalid-name
            [enabled, effect, mode, r, g, b, warmness, brightness] = message['body']
            return {
                'enabled': enabled == 1,
                'effect': Effect(effect),
                'mode': Mode(mode),
                'color': (r, g, b),
                'warmness': warmness,
                'brightness': brightness,
            }
        else:
            raise UnknownCommandError()

    async def set_color(self, color: RGBColor):
        """Set backlight rgb color"""
        return await self.send(Command.SET_COLOR, *color)

    async def set_white(self, warmness: Byte) -> bool:
        """Set backlight white color"""
        return await self.send(Command.SET_WHITE, warmness)

    async def set_brightness(self, brightness: Byte) -> bool:
        """Set backlight brightness"""
        return await self.send(Command.SET_BRIGHTNESS, brightness)

    async def set_effect(self, effect: Effect) -> bool:
        """Set backlight effect"""
        return await self.send(Command.SET_EFFECT, effect.value)

    async def set_power(self, is_on: bool) -> bool:
        """Set backlight power state"""
        return await self.send(Command.SET_POWER, 1 if is_on else 0)

    async def update_firmware(self,
        hex_content: bytes,
        reporter: Optional[ProgressReporter] = None
    ):
        """Flashes Intel HEX formatted firmware to backlight"""
        firmware = Firmware(hex_content.decode())
        is_invited = await self.send(
            Command.FIRMWARE_RECEIVE,
            high_byte(firmware.size),
            low_byte(firmware.size)
        )
        if not is_invited:
            return
        def report_progress (val: float) -> None:
            if reporter is not None:
                reporter(val)
        pages = firmware.pages
        progress = 0
        percent = 98 / len(pages)
        for page in pages:
            (_, success) = await self.send(
                Command.FIRMWARE_FRAME,
                *page,
                111
            )
            if not success:
                raise FirmwareError("frame is not received")
            progress += percent
            report_progress(progress)
        (_, success) = await self.send_request(Command.FIRMWARE_APPLY)
        if not success:
            raise FirmwareError("firmware cannot be applied")
        await wait_for(self._stream.host_down(), 15)
        report_progress(99)
        await wait_for(self._stream.host_up(), 10)
        report_progress(100)
