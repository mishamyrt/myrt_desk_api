"""MyrtDesk backlight controller"""
from asyncio import wait_for
from typing import List, Tuple, Callable
from ..bytes import high_byte, low_byte
from ..domain import MyrtDeskDomain
from .firmware import Firmware
from .ping import host_down, host_up
from .constants import (
    DOMAIN_BACKLIGHT,
    COMMAND_SET_COLOR,
    COMMAND_SET_WHITE,
    COMMAND_SET_EFFECT,
    COMMAND_SET_BRIGHTNESS,
    COMMAND_FIRMWARE_RECEIVE,
    COMMAND_FIRMWARE_FRAME,
    COMMAND_FIRMWARE_APPLY,
    COMMAND_TURN_OFF,
    COMMAND_READ_STATE
)

RGBColor = Tuple[int, int, int]

class MyrtDeskBacklight(MyrtDeskDomain):
    """MyrtDesk backlight controller constructor"""
    _domain_code = DOMAIN_BACKLIGHT

    async def read_state(self):
        """Reads backlight state"""
        (data, success) = await self._send_command([COMMAND_READ_STATE])
        if not success:
            return None
        # pylint: disable-next=invalid-name
        [_, _, _, enabled, effect, mode, r, g, b, warmness, brightness] = data
        return {
            'enabled': enabled == 1,
            'effect': effect,
            'mode': mode,
            'color': (r, g, b),
            'warmness': warmness,
            'brightness': brightness,
        }

    async def update_firmware(self, hex_content: bytes, reporter: Callable = None):
        """Flashes Intel HEX formatted firmware to backlight"""
        firmware = Firmware(hex_content.decode())
        (_, success) = await self._send_command([
            COMMAND_FIRMWARE_RECEIVE,
            high_byte(firmware.size),
            low_byte(firmware.size)
        ])
        def report_progress (val: float) -> None:
            if reporter is not None:
                reporter(val)
        pages = firmware.pages
        progress = 0
        percent = 98 / len(pages)
        for page in pages:
            (_, success) = await self._send_command([
                COMMAND_FIRMWARE_FRAME,
                *page,
                111
            ])
            if not success:
                raise Exception()
            progress += percent
            report_progress(progress)
        (_, success) = await self._send_command([COMMAND_FIRMWARE_APPLY])
        if not success:
            raise Exception()
        host = self._transport.host
        await wait_for(host_down(host), 15)
        report_progress(99)
        await wait_for(host_up(host), 10)
        report_progress(100)

    # pylint: disable-next=invalid-name
    async def set_color(self, color: RGBColor):
        """Set backlight rgb color"""
        (_, success) = await self._send_command([COMMAND_SET_COLOR, *color])
        return success

    async def set_white(self, warmness: int) -> bool:
        """Set backlight white color"""
        (_, success) = await self._send_command([COMMAND_SET_WHITE, warmness])
        return success

    async def set_brightness(self, brightness: int) -> bool:
        """Set backlight brightness"""
        (_, success) = await self._send_command([COMMAND_SET_BRIGHTNESS, brightness])
        return success

    async def set_effect(self, brightness: int) -> bool:
        """Set backlight effect"""
        (_, success) = await self._send_command([COMMAND_SET_EFFECT, brightness])
        return success