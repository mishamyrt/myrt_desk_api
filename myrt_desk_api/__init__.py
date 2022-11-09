"""MyrtDesk controller"""
from .transport import MyrtDeskTransport
from .backlight import MyrtDeskBacklight, Effect
from .system import MyrtDeskSystem
from .legs import MyrtDeskLegs
from .discover import discover

__version__ = "0.0.1"

class MyrtDesk:
    """MyrtDesk controller entity"""
    _transport: MyrtDeskTransport
    _backlight: MyrtDeskBacklight
    _system: MyrtDeskSystem
    _legs: MyrtDeskLegs

    def __init__(self, host: str):
        self._transport = MyrtDeskTransport(host)
        self._backlight = MyrtDeskBacklight(self._transport)
        self._legs = MyrtDeskLegs(self._transport)
        self._system = MyrtDeskSystem(self._transport)

    @property
    def backlight(self) -> MyrtDeskBacklight:
        """MyrtDesk backlight controller"""
        return self._backlight

    @property
    def system(self) -> MyrtDeskSystem:
        """MyrtDesk system controller"""
        return self._system

    @property
    def legs(self) -> MyrtDeskLegs:
        """MyrtDesk legs controller"""
        return self._legs
