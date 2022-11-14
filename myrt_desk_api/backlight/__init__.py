"""MyrtDesk backlight controller"""
from asyncio import wait_for
from typing import List, Tuple, Callable
from ..ping import host_down, host_up
from ..bytes import high_byte, low_byte
from ..domain import MyrtDeskDomain
from .firmware import Firmware
from .effects import Effect
from .constants import (
    DOMAIN_BACKLIGHT,
    COMMAND_SET_COLOR,
    COMMAND_SET_WHITE,
    COMMAND_SET_EFFECT,
    COMMAND_SET_EFFECT_DATA,
    COMMAND_SET_BRIGHTNESS,
    COMMAND_FIRMWARE_RECEIVE,
    COMMAND_FIRMWARE_FRAME,
    COMMAND_FIRMWARE_APPLY,
    COMMAND_SET_POWER,
    COMMAND_READ_STATE
)

RGBColor = Tuple[int, int, int]
AmbientZone = Tuple[int, int]

class MyrtDeskBacklight(MyrtDeskDomain):
    """MyrtDesk backlight controller constructor"""
    _domain_code = DOMAIN_BACKLIGHT

    async def read_state(self):
        """Reads backlight state"""
        (data, success) = await self.send_command([COMMAND_READ_STATE])
        if not success:
            return None
        # pylint: disable-next=invalid-name
        [_, _, _, enabled, effect, mode, r, g, b, warmness, brightness] = data
        return {
            'enabled': enabled == 1,
            'effect': Effect(effect),
            'mode': mode,
            'color': (r, g, b),
            'warmness': warmness,
            'brightness': brightness,
        }

    async def update_firmware(self, hex_content: bytes, reporter: Callable = None):
        """Flashes Intel HEX formatted firmware to backlight"""
        firmware = Firmware(hex_content.decode())
        (_, success) = await self.send_command([
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
            (_, success) = await self.send_command([
                COMMAND_FIRMWARE_FRAME,
                *page,
                111
            ])
            if not success:
                raise Exception()
            progress += percent
            report_progress(progress)
        (_, success) = await self.send_command([COMMAND_FIRMWARE_APPLY])
        if not success:
            raise Exception()
        host = self._transport.host
        await wait_for(host_down(host), 15)
        report_progress(99)
        await wait_for(host_up(host), 10)
        report_progress(100)

    async def set_color(self, color: RGBColor):
        """Set backlight rgb color"""
        (_, success) = await self.send_command([COMMAND_SET_COLOR, *color])
        return success

    async def start_ambient(self, zones: List[AmbientZone]) -> bool:
        """Start ambient effect with zones"""
        payload = []
        for zone in zones:
            payload.append(zone[0])
            payload.append(zone[1])
        (_, success) = await self.send_command([
            COMMAND_SET_EFFECT,
            Effect.AMBIENT,
            len(zones),
            *payload
        ])
        return success

    async def set_ambient_colors(self, colors: List[RGBColor]) -> bool:
        """Sets ambient effect colors"""
        payload = []
        for color in colors:
            payload.append(color[0])
            payload.append(color[1])
            payload.append(color[2])
        await self.send_command([COMMAND_SET_EFFECT_DATA, *payload])

    async def set_white(self, warmness: int) -> bool:
        """Set backlight white color"""
        (_, success) = await self.send_command([COMMAND_SET_WHITE, warmness])
        return success

    async def set_brightness(self, brightness: int) -> bool:
        """Set backlight brightness"""
        (_, success) = await self.send_command([COMMAND_SET_BRIGHTNESS, brightness])
        return success

    async def set_effect(self, brightness: int) -> bool:
        """Set backlight effect"""
        (_, success) = await self.send_command([COMMAND_SET_EFFECT, brightness])
        return success

    async def set_power(self, is_on: bool) -> bool:
        """Set backlight power state"""
        (_, success) = await self.send_command([COMMAND_SET_POWER, 1 if is_on else 0])
        return success
