from enum import Enum
from typing import Callable, Tuple

from typing_extensions import TypedDict

from myrt_desk_api.transport import Byte

DOMAIN_BACKLIGHT = 1

class Effect(Enum):
    """MyrtDesk backlight effects"""
    NONE = 0
    RAINBOW = 1
    PROGRESS = 2
    AMBIENT = 3
    GRADIENT = 4

class Command(Enum):
    """MyrtDesk backlight commands"""
    READ_STATE = 0
    SET_EFFECT = 1
    SET_EFFECT_DATA = 2
    SET_COLOR = 3
    SET_WHITE = 4
    SET_BRIGHTNESS = 5
    SET_POWER = 6
    FIRMWARE_RECEIVE = 7
    FIRMWARE_FRAME = 8
    FIRMWARE_APPLY = 9
    BROADCAST_STATE = 10

class Mode(Enum):
    """MyrtDesk modes"""
    RGB = 0
    TEMPERATURE = 1

RGBColor = Tuple[int, int, int]

AmbientZone = Tuple[int, int]

State = TypedDict('SocketMessage', {
    'enabled': bool,
    'effect': Effect,
    'mode': Mode,
    'color': RGBColor,
    'warmness': Byte,
    'brightness': Byte,
})

ProgressReporter = Callable[[float], None]
