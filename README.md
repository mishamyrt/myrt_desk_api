# MyrtDesk API [![PyPI version](https://badge.fury.io/py/myrt-desk-api.svg)](https://pypi.org/project/myrt-desk-api/)

Library for controlling smart table functions with my own [firmware](https://github.com/mishamyrt/myrt_desk_firmware).

* **Fully asynchronous**
* Automatic detection
* Cool CLI tool

## API Example
This code will wait for the lights to turn off, then flash the backlight controller and then turn on the rainbow effect:

```py
from asyncio import run
from myrt_desk_api import MyrtDesk, Effect

async def main():
    desk_host = await discover()
    desk = MyrtDesk(desk_host)
    await desk.backlight.set_power(False)
    with open("./firmware.hex", mode="rb") as file:
        await desk.backlight.update_firmware(file.read())
    await desk.backlight.set_effect(Effect.RAINBOW)

if __name__ == '__main__':
    run(main())
```