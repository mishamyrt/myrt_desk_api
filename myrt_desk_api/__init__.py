"""MyrtDesk controller"""
from .backlight import Effect, MyrtDeskBacklight
from .legs import MyrtDeskLegs
from .system import MyrtDeskSystem
from .transport import Stream

__version__ = "0.2.0"

class MyrtDesk:
    """MyrtDesk controller entity"""
    _stream: Stream
    _backlight: MyrtDeskBacklight
    _system: MyrtDeskSystem
    _legs: MyrtDeskLegs

    def __init__(self, host="MyrtDesk.local"):
        stream = Stream(host)
        self._stream = stream
        self._backlight = MyrtDeskBacklight(stream)
        self._legs = MyrtDeskLegs(stream)
        self._system = MyrtDeskSystem(stream)

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
